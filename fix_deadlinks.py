import os, re

REPO = r"C:\Users\77281\Desktop\文档站\biliup-docs"
GUIDE = os.path.join(REPO, "docs", "guide")

OLD2NEW = {
    "GlobalConfig": "global-config",
    "liveconfig": "live-config",
    "developerOptions": "developer-options",
    "supportedLivePlatforms": "supported-platforms",
}

# basename(无.md) -> 相对 GUIDE 的路径(无后缀)，如 "配置/global-config"
BASENAME_MAP = {}
for root, dirs, files in os.walk(GUIDE):
    if ".vitepress" in root:
        continue
    for f in files:
        if f.endswith(".md"):
            base = f[:-3]
            rel = os.path.relpath(os.path.join(root, f), GUIDE)[:-3]
            BASENAME_MAP[base] = rel.replace(os.sep, "/")


def rewrite(tgt, src_rel):
    tgt = tgt.strip()
    if tgt.startswith(("#", "http://", "https://", "mailto:")):
        return None
    anchor = ""
    if "#" in tgt:
        tgt, anchor = tgt.split("#", 1)
        anchor = "#" + anchor
    suffix = ""
    if tgt.endswith(".html"):
        suffix = ".html"
        tgt = tgt[:-5]
    elif tgt.endswith(".md"):
        suffix = ".md"
        tgt = tgt[:-3]

    if tgt.startswith("/"):
        # 绝对路径 /guide/配置/GlobalConfig.html
        inner = tgt[1:]                      # guide/配置/GlobalConfig
        base = inner.rstrip("/").split("/")[-1]
        if base not in OLD2NEW:
            return None
        newbase = OLD2NEW[base]
        if newbase not in BASENAME_MAP:
            return None
        newrel = BASENAME_MAP[newbase]       # 配置/global-config
        return "/guide/" + newrel + suffix + anchor

    base = tgt.rstrip("/").split("/")[-1]
    if base not in OLD2NEW:
        return None
    newbase = OLD2NEW[base]
    if newbase not in BASENAME_MAP:
        return None
    newrel = BASENAME_MAP[newbase]           # 配置/global-config
    new_dir = os.path.dirname(newrel)
    src_dir = os.path.dirname(src_rel)
    rel = os.path.relpath(new_dir, src_dir).replace(os.sep, "/")
    if rel == ".":
        result = "./" + newbase
    else:
        result = rel + "/" + newbase
    return result + suffix + anchor


MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
HTML_HREF = re.compile(r'href="([^"]+)"')

changed_files = 0
total = 0
for root, dirs, files in os.walk(GUIDE):
    if ".vitepress" in root:
        continue
    for f in files:
        if not f.endswith(".md"):
            continue
        path = os.path.join(root, f)
        src_rel = os.path.relpath(path, GUIDE)[:-3].replace(os.sep, "/")
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            continue
        newtext = text

        def md_repl(m, sr=src_rel):
            res = rewrite(m.group(1), sr)
            return m.group(0) if res is None else "](" + res + ")"

        def html_repl(m, sr=src_rel):
            res = rewrite(m.group(1), sr)
            return m.group(0) if res is None else 'href="' + res + '"'

        newtext = MD_LINK.sub(md_repl, newtext)
        newtext = HTML_HREF.sub(html_repl, newtext)

        if newtext != text:
            open(path, "w", encoding="utf-8").write(newtext)
            changed_files += 1
            total += len(re.findall(r"global-config|live-config|developer-options|supported-platforms", newtext)) - len(re.findall(r"global-config|live-config|developer-options|supported-platforms", text))
            print("fixed:", src_rel)

print(f"[done] {changed_files} 文件被修改")
