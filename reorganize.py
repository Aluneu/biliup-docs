# -*- coding: utf-8 -*-
import os, shutil, re, json

REPO = r"C:/Users/77281/Desktop/文档站/biliup-docs"
ROOT = os.path.join(REPO, "docs", "guide")
INTRO = os.path.join(ROOT, "introduce")

# ---------- 0. 备份（出错可恢复） ----------
backup = "/tmp/biliup_docs_backup"
if os.path.exists(backup):
    shutil.rmtree(backup)
shutil.copytree(ROOT, backup)
print("BACKUP ->", backup)

# ---------- 1. 建新分组目录（平台配置 由 live rename 产生，不预建） ----------
for d in ["上手", "安装部署", "配置", "进阶运行", "帮助", "更多"]:
    os.makedirs(os.path.join(INTRO, d), exist_ok=True)

def move(src, dst):
    s = os.path.join(ROOT, src)
    d = os.path.join(ROOT, dst)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.move(s, d)
    print("MOVE", src, "->", dst)

# 上手
move("introduce/introduce/introduce.md", "introduce/上手/introduce.md")
move("introduce/introduce/supportedLivePlatforms.md", "introduce/上手/supportedLivePlatforms.md")
move("introduce/quickstart/get-start.md", "introduce/上手/get-start.md")
# 安装部署
move("introduce/introduce/Linux.md", "introduce/安装部署/Linux.md")
move("introduce/introduce/windows.md", "introduce/安装部署/windows.md")
move("introduce/introduce/macos.md", "introduce/安装部署/macos.md")
move("introduce/introduce/termux.md", "introduce/安装部署/termux.md")
move("introduce/introduce/docker.md", "introduce/安装部署/docker.md")
move("docs/ffmpeg安装.md", "introduce/安装部署/ffmpeg安装.md")
# 配置
move("introduce/introduce/login.md", "introduce/配置/login.md")
move("introduce/Config/GlobalConfig.md", "introduce/配置/GlobalConfig.md")
move("introduce/Config/liveconfig.md", "introduce/配置/liveconfig.md")
move("introduce/Config/developerOptions.md", "introduce/配置/developerOptions.md")
move("基础配置/首次运行.md", "introduce/配置/首次运行.md")
# 平台配置（live 整目录改名）
shutil.move(os.path.join(INTRO, "live"), os.path.join(INTRO, "平台配置"))
print("RENAME live -> 平台配置")
# 进阶运行
move("进阶运行/p.md", "introduce/进阶运行/p.md")
# 帮助
move("introduce/introduce/faq.md", "introduce/帮助/faq.md")
move("introduce/introduce/credits.md", "introduce/帮助/credits.md")
move("help.md", "introduce/帮助/help.md")
# 更多
move("introduce/introduce/architecture.md", "introduce/更多/architecture.md")
move("introduce/introduce/biliup-app.md", "introduce/更多/biliup-app.md")

# ---------- 2. 链接修正 ----------
rules = [
    (r'\.\./introduce/introduce/supportedLivePlatforms', r'../上手/supportedLivePlatforms'),
    (r'\.\./introduce/supportedLivePlatforms', r'../上手/supportedLivePlatforms'),
    (r'\.\./introduce/login', r'../配置/login'),
    (r'\.\./Config/', r'../配置/'),
    (r'\./Config/', r'../配置/'),
    (r'\.\./\.\./docs/ffmpeg安装', r'../安装部署/ffmpeg安装'),
    (r'\./login\.html', r'../配置/login.html'),
    (r'\./Linux\.html', r'../安装部署/Linux.html'),
    (r'\./windows\.html', r'../安装部署/windows.html'),
    (r'\./docker\.html', r'../安装部署/docker.html'),
    (r'\./macos\.html', r'../安装部署/macos.html'),
    (r'\./faq\.html', r'../帮助/faq.html'),
    (r'\.\./quickstart/get-start\.html', r'../上手/get-start.html'),
    (r'\.\./\.\./help\.html', r'../帮助/help.html'),
]

def fix_dir(dp):
    for fn in os.listdir(dp):
        fp = os.path.join(dp, fn)
        if os.path.isdir(fp):
            fix_dir(fp)
        elif fn.endswith('.md'):
            with open(fp, encoding='utf-8') as f:
                t = f.read()
            o = t
            for pat, rep in rules:
                t = re.sub(pat, rep, t)
            if t != o:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(t)
                print("FIX", os.path.relpath(fp, ROOT))

fix_dir(INTRO)

# ---------- 3. 清理空目录 + 删除冗余桩目录 ----------
for d in ["introduce/introduce", "introduce/quickstart", "introduce/Config", "基础配置", "进阶运行"]:
    p = os.path.join(ROOT, d)
    if os.path.exists(p):
        shutil.rmtree(p); print("RM", d)
stub = os.path.join(ROOT, "安装部署")
if os.path.exists(stub):
    shutil.rmtree(stub); print("RM 安装部署(stub)")

# ---------- 4. mapping.json ----------
mj = os.path.join(ROOT, "mapping.json")
with open(mj, encoding='utf-8-sig') as f:
    m = json.load(f)
for k in ["introduce", "quickstart", "Config", "live", "参数详解", "基础配置"]:
    m.pop(k, None)
if m.get("安装部署") == "安装":
    m["安装部署"] = "安装部署"
if m.get("进阶运行") == "进阶":
    m["进阶运行"] = "进阶运行"
for k in ["上手", "配置", "平台配置", "帮助", "更多"]:
    m[k] = k
with open(mj, 'w', encoding='utf-8') as f:
    json.dump(m, f, ensure_ascii=False, separators=(',', ':'))

# ---------- 5. config.mts ----------
cfg = os.path.join(REPO, "docs", ".vitepress", "config.mts")
with open(cfg, encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'\s*"/guide/introduce/Config/": set_sidebar\([^)]*\),\n', '', c)
c = re.sub(r'\s*"/guide/introduce/live/": set_sidebar\([^)]*\),\n', '', c)
c = re.sub(r'\s*"/guide/安装部署/": set_sidebar\([^)]*\),\n', '', c)
c = re.sub(r"set_sidebar\('/guide/([^']+)', false\)", r"set_sidebar('/guide/\1', false, true)", c)
with open(cfg, 'w', encoding='utf-8') as f:
    f.write(c)

print("ALL DONE")
