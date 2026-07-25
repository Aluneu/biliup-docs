#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 页面命名优化脚本：introduce -> getting-started，英文文件名转 kebab-case。
# 运行：python rename_pages.py   （需在 biliup-docs 仓库目录下，且已装好依赖无关）
import os, re, json, shutil, subprocess

REPO = os.path.dirname(os.path.abspath(__file__))
DOCS_GUIDE = os.path.join(REPO, "docs", "guide")
GUIDE_PREFIX = "docs/guide/"

def gmove(src, dst):
    """优先 git mv（保留 rename 记录），失败则 shutil.move。"""
    try:
        r = subprocess.run(["git", "-C", REPO, "mv", src, dst],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return
    except Exception:
        pass
    shutil.move(src, dst)

# ---------- 1. 收集当前所有 .md 相对路径（under docs/guide） ----------
old_list = []
for root, dirs, files in os.walk(DOCS_GUIDE):
    if ".vitepress" in root or "node_modules" in root:
        continue
    for f in files:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, f), DOCS_GUIDE).replace(os.sep, "/")
            old_list.append(rel)
old_list.sort()

FILE_RENAMES = {
    "getting-started/上手/introduce.md": "getting-started/上手/index.md",
    "getting-started/上手/supportedLivePlatforms.md": "getting-started/上手/supported-platforms.md",
    "getting-started/配置/GlobalConfig.md": "getting-started/配置/global-config.md",
    "getting-started/配置/liveconfig.md": "getting-started/配置/live-config.md",
    "getting-started/配置/developerOptions.md": "getting-started/配置/developer-options.md",
    "getting-started/更多/biliup-app.md": "getting-started/更多/desktop-app.md",
    "getting-started/进阶运行/p.md": "getting-started/进阶运行/advanced.md",
    "docs/doc.md": "docs/overview.md",
}

def new_rel_of(old_rel):
    r = old_rel
    if r.startswith("introduce/"):
        r = "getting-started/" + r[len("introduce/"):]
    if r in FILE_RENAMES:
        r = FILE_RENAMES[r]
    return r

old2new = {o: new_rel_of(o) for o in old_list}
new2old = {v: k for k, v in old2new.items()}
old_dirs = {os.path.dirname(o) for o in old_list}

print(f"[info] 当前 .md 文件数: {len(old_list)}")

# ---------- 2. 移动文件 ----------
gmove(os.path.join(DOCS_GUIDE, "introduce"),
      os.path.join(DOCS_GUIDE, "getting-started"))
moved = 0
for o, n in FILE_RENAMES.items():
    src = os.path.join(DOCS_GUIDE, o)
    dst = os.path.join(DOCS_GUIDE, n)
    if os.path.exists(src) and not os.path.exists(dst):
        gmove(src, dst)
        moved += 1
print(f"[info] 文件重命名: {moved}")

# ---------- 3. 更新 mapping.json ----------
mpath = os.path.join(DOCS_GUIDE, "mapping.json")
with open(mpath, encoding="utf-8") as f:
    raw = f.read()
data = json.loads(raw.lstrip("\ufeff"))
key_map = {
    "introduce.md": None,
    "GlobalConfig.md": "global-config.md",
    "liveconfig.md": "live-config.md",
    "developerOptions.md": "developer-options.md",
    "supportedLivePlatforms.md": "supported-platforms.md",
    "biliup-app.md": "desktop-app.md",
    "p.md": "advanced.md",
    "doc.md": "overview.md",
}
new_data = {}
for k, v in data.items():
    if k == "introduce.md":
        continue
    new_data[key_map.get(k, k)] = v
new_data["上手/index.md"] = "介绍"
new_data["index.md"] = "介绍"  # 供 sortOrder 白名单过滤 & fallback 使用

# 为所有 index.md 文件补 path-specific 键，避免裸 index.md 串味到其它 index 页
for rel in old2new.values():
    if rel.endswith("/index.md") and rel not in new_data:
        fpath = os.path.join(DOCS_GUIDE, rel)
        title = os.path.splitext(os.path.basename(rel))[0]
        try:
            with open(fpath, encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
        except Exception:
            pass
        new_data[rel] = title
        print(f"[info] 为 {rel} 补映射: {title}")

with open(mpath, "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, separators=(",", ":"))
print("[info] mapping.json 已更新")

# ---------- 4. 更新 config.mts ----------
cpath = os.path.join(REPO, "docs", ".vitepress", "config.mts")
with open(cpath, encoding="utf-8") as f:
    ct = f.read()
ct = ct.replace("/guide/introduce/", "/guide/getting-started/")
ct = ct.replace("set_sidebar('/guide/introduce'", "set_sidebar('/guide/getting-started'")
ct = ct.replace("/guide/getting-started/上手/introduce", "/guide/getting-started/上手/")
with open(cpath, "w", encoding="utf-8") as f:
    f.write(ct)
print("[info] config.mts 已更新")

# ---------- 4b. 更新首页 docs/index.md 的 hero/features 链接（不在 docs/guide 下，需单独处理） ----------
ipath = os.path.join(REPO, "docs", "index.md")
with open(ipath, encoding="utf-8") as f:
    it = f.read()
# 先处理具体的 上手/introduce（改成目录链接），再做通用前缀替换，避免顺序出错
it = it.replace("/guide/introduce/上手/introduce", "/guide/getting-started/上手/")
it = it.replace("/guide/introduce/", "/guide/getting-started/")
with open(ipath, "w", encoding="utf-8") as f:
    f.write(it)
print("[info] docs/index.md 已更新")

# ---------- 5. 重写所有 .md 内部链接 ----------
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
HTML_RE = re.compile(r'<a\s+href=(["\'])([^"\']+)\1>')

def normalize(p):
    return os.path.normpath(p).replace(os.sep, "/")

def resolve_base(base, s_old_dir):
    if base.startswith("/"):
        abs = normalize("docs" + base)          # /guide/X -> docs/guide/X
    else:
        abs = normalize(s_old_dir + "/" + base)
    rel = abs[len(GUIDE_PREFIX):]
    if (rel + ".md") in old2new:
        return rel + ".md"
    if rel in old2new:
        return rel
    for idx in ("/index.md", "/introduce.md", "/README.md"):
        if (rel + idx) in old2new:
            return rel + idx
    return None

def rewrite_target(target, s_new_dir, s_old_dir):
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    frag = ""
    if "#" in target:
        target, frag = target.split("#", 1)
    query = ""
    if "?" in target:
        target, query = target.split("?", 1)
    if target == "":
        return None
    if target.endswith(".html"):
        base, style = target[:-5], ".html"
    elif target.endswith(".md"):
        base, style = target[:-3], ".html"
    elif target.endswith("/"):
        base, style = target[:-1], "/"
    else:
        base, style = target, ""
    old_md = resolve_base(base, s_old_dir)
    if old_md is None:
        return ("UNRESOLVED", target)
    new_md = old2new[old_md]
    new_file_abs = os.path.join(DOCS_GUIDE, new_md)
    if style == ".html":
        if base.startswith("/"):
            np_ = "/guide/" + new_md[:-3] + ".html"
        else:
            rp = os.path.relpath(new_file_abs, s_new_dir).replace(os.sep, "/")
            np_ = rp[:-3] + ".html"
    elif style == "/":
        dir_abs = os.path.dirname(new_file_abs)
        if base.startswith("/"):
            np_ = "/guide/" + os.path.dirname(new_md)
        else:
            np_ = os.path.relpath(dir_abs, s_new_dir).replace(os.sep, "/") + "/"
    else:
        if base.startswith("/"):
            np_ = "/guide/" + new_md[:-3]
        else:
            rp = os.path.relpath(new_file_abs, s_new_dir).replace(os.sep, "/")
            np_ = rp[:-3]
    if query:
        np_ += "?" + query
    if frag:
        np_ += "#" + frag
    return np_

changed_files = 0
unresolved = []
for new_rel in sorted(old2new.values()):
    fpath = os.path.join(DOCS_GUIDE, new_rel)
    if not os.path.exists(fpath):
        continue
    with open(fpath, encoding="utf-8") as f:
        content = f.read()
    s_new_dir = os.path.dirname(fpath)
    s_old_dir = os.path.dirname(os.path.join(DOCS_GUIDE, new2old[new_rel]))
    def repl(m):
        tgt = m.group(1)
        res = rewrite_target(tgt, s_new_dir, s_old_dir)
        if res is None or res == tgt:
            return m.group(0)
        if isinstance(res, tuple) and res[0] == "UNRESOLVED":
            unresolved.append((new_rel, res[1]))
            return m.group(0)
        return "](" + res + ")"
    def repl_html(m):
        q, tgt = m.group(1), m.group(2)
        res = rewrite_target(tgt, s_new_dir, s_old_dir)
        if res is None or res == tgt:
            return m.group(0)
        if isinstance(res, tuple) and res[0] == "UNRESOLVED":
            unresolved.append((new_rel, res[1]))
            return m.group(0)
        return f'<a href={q}{res}{q}'
    new_content = LINK_RE.sub(repl, content)
    new_content = HTML_RE.sub(repl_html, new_content)
    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        changed_files += 1

print(f"[info] 重写链接的文件数: {changed_files}")
print(f"[info] 无法解析的链接数: {len(unresolved)}")
for u in unresolved[:40]:
    print("   UNRESOLVED", u)

# ---------- 6. 自检：扫描残留旧路径 ----------
STALE = ["introduce/", "GlobalConfig", "liveconfig", "developerOptions",
         "supportedLivePlatforms", "/p.md", "doc.md"]
leftover = 0
# 额外扫描 docs/index.md 与 config.mts（脚本显式处理过，确认无残留）
extra_files = [os.path.join(REPO, "docs", "index.md"),
               os.path.join(REPO, "docs", ".vitepress", "config.mts")]
for p in extra_files:
    if os.path.exists(p):
        try:
            txt = open(p, encoding="utf-8").read()
        except Exception:
            continue
        for s in STALE:
            if s in txt:
                print(f"   残留 {s} -> {os.path.relpath(p, REPO)}")
                leftover += 1
                break
for root, dirs, files in os.walk(DOCS_GUIDE):
    if ".vitepress" in root:
        continue
    for f in files:
        if f.endswith(".md"):
            p = os.path.join(root, f)
            try:
                txt = open(p, encoding="utf-8").read()
            except Exception:
                continue
            for s in STALE:
                if s in txt:
                    print(f"   残留 {s} -> {os.path.relpath(p, REPO)}")
                    leftover += 1
                    break
print(f"[info] 残留旧路径命中: {leftover}")
print("[done] 完成。请运行 npm run docs:build 验证，再 git add docs/ && git commit")
