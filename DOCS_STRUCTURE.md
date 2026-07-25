# biliup 文档站结构说明（维护指南）

> 写给要给文档站加页面、改侧边栏的维护者。站点本身以 biliup 源码与 VitePress 配置为准，本文只讲本仓库的约定。

## 技术栈与目录

- 框架：[VitePress](https://vitepress.dev/)，源码根目录 `docs/`
- 站点配置：`docs/.vitepress/config.mts`
- 主题与样式：`docs/.vitepress/theme/`（`custom.css` 是自定义样式唯一入口）
- 侧边栏生成：`docs/guide/set_sidebar.mts` + `docs/guide/mapping.json`
- 构建：`npm run docs:build`；本地预览：`npm run docs:dev`
- 部署：推送到 `main` 分支后由 GitHub Actions 自动构建发布

> `dist/` 是构建产物，已被 gitignore，无需提交。

## 侧边栏是自动生成的

侧边栏不是手写，由 `set_sidebar.mts` 扫描 `docs/guide/` 目录树生成：

- 每个 `.md` 在侧边栏的**显示名**取自 `mapping.json` 的键 `"文件名.md"`。
- 缺条目时回退显示成文件名本身（带 `.md`）——这是“侧边栏怪名”的常见原因。
- 目录层级 = 侧边栏分组层级；分组与条目顺序由 `mapping.json` 的键顺序决定。

### 新增一个页面

1. 在 `docs/guide/` 下合适子目录新建 `xxx.md`。
2. 在 `mapping.json` 追加一条 `"xxx.md": "显示名"`（键的先后位置会影响它在侧边栏里的排序）。
3. 跑 `npm run docs:build`，确认侧边栏显示的是“显示名”而不是“xxx.md”。

## 内部链接写法

VitePress 线上 URL 镜像源码目录结构，写内部链接时：

- 用 `.html` 后缀（不是 `.md`）。
- 相对路径的 `../` 层数要数对，错一级就 404。

> 构建已开启死链检查，链接写错会在 `docs:build` 阶段直接报错，不用手动扫。

## 样式

- 自定义样式唯一入口：`docs/.vitepress/theme/custom.css`。
- 配色走 VitePress 设计变量（`--vp-c-*`），明暗主题自动适配，不要硬编码颜色。
- 首页是唯一用自定义 HTML + CSS 装饰的页面，改样式请复用 `custom.css` 已有的类，不要新造。

## 改文档的标准流程

- [ ] 在 `docs/guide/` 对应子目录新建 / 编辑 `.md`
- [ ] 新页面：在 `mapping.json` 加 `"文件名.md": "显示名"`
- [ ] 内部链接用 `.html` 后缀、数清 `../`
- [ ] `npm run docs:build` 通过（0 错误、无死链）
- [ ] 推 `main` 触发自动部署
