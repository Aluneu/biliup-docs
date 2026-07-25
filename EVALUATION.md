# biliup 文档站评估报告

评估对象：`C:\Users\77281\Desktop\文档站\biliup-docs`（VitePress 文档站）
评估日期：2026-07-26
评估范围：信息架构、技术健康度、内容一致性、团队可维护性、部署发布

---

## 总评

文档站内容覆盖广（20+ 平台、安装/配置/API/开发指南齐全），首页指引页设计精致，CI 部署链路完整。但有几类问题在**团队维护**场景下会被持续放大：门面元数据还是模板默认、死链检查被全局关掉、结构说明文档严重过时、callout 语法两套并存。

整体健康度：**中等偏上，但有几处该尽快收口**。

| 维度 | 评分 | 一句话 |
|---|---|---|
| 信息架构与导航 | 3.5 / 5 | 分组合理，但侧边栏顺序乱、默认全折叠 |
| 技术健康度 | 3 / 5 | 死链开关关闭、base 路径矛盾待确认、package.json 陈旧 |
| 内容一致性 | 2.5 / 5 | callout 语法两套、结构说明文档过时、语气不统一 |
| 团队可维护性 | 2.5 / 5 | 一次性脚本硬编码个人路径入库、加页约定隐性、editLink 关闭 |
| 部署发布 | 3.5 / 5 | CI 完整，但 base/CNAME 待确认 |

---

## P0 — 高风险，建议先处理

### 1. package.json 仍是模板默认元数据
**证据**：`package.json`
- `name: "moyu-docs"`
- `description: "MoYu框架文档"`
- `author: { name: "少林寺驻北固山办事处大神父王喇嘛", ... }`（个人网名）
- `homepage: "https://gitee.com/dotnetmoyu/Vitepress-Template"`（模板来源）

**影响**：站点本身已品牌化为 BiliuP（`config.mts` 的 title/nav 都指向 biliup），但 npm 元数据和仓库门面仍显示为某个第三方模板。任何看 `package.json` 或 GitHub 仓库描述的人会被误导。

**建议**：
- `name` 改为 `biliup-docs`
- 加 `repository` / `bugs` 指向 biliup-docs 仓库
- `author` 改为组织名或删除，`description` 重写为 biliup 文档站
- 确认 `license: MIT` 是否真的适用（内容归属 biliup 项目，需与上游一致）

### 2. `ignoreDeadLinks: true` 全局关闭死链检查
**证据**：`docs/.vitepress/config.mts:22`
```ts
ignoreDeadLinks: true,
```
同时 `DOCS_STRUCTURE.md:164` 的 checklist 却写着"跑 `npm run docs:build` 确认 0 错误、**无死链**"——自相矛盾。

**影响**：所有内部死链都不会在构建时报错。文档站采用"内部链接用 `.html` 后缀 + 数 `../` 层数"的脆弱约定（见 DOCS_STRUCTURE 第 4 节），多人协作后死链会静默累积，且无人能在 CI 发现。

**建议**：删掉 `ignoreDeadLinks: true`（恢复默认检查），或仅对已知外链做白名单。若担心构建因历史死链失败，先用脚本扫一遍现存死链再开。

### 3. 部署 base 路径矛盾（待确认线上是否 404）
**证据**：
- `config.mts:9`：`base: "/"`（注释假定"自定义域名下站点在根目录"）
- `DOCS_STRUCTURE.md:14`：写的是 `base: /biliup-docs/`
- 仓库内**无 `CNAME` 文件**，`deploy.yml` 也**无添加 CNAME 的步骤**
- `DOCS_STRUCTURE.md:13`：部署地址写 `https://aluneu.github.io/biliup-docs/`

**影响**：若实际部署到 `aluneu.github.io/biliup-docs/`（project page，无自定义域名），`base: "/"` 会导致所有 CSS/JS/资源 404，整站样式与交互失效。若已配自定义域名则 OK，但文档与配置仍互相矛盾。

**建议**：确认线上域名。用自定义域名 → 在 Pages 设置或加 `CNAME` 文件，并同步更新 DOCS_STRUCTURE；用 project page → `base` 改回 `/biliup-docs/`。

---

## P1 — 中风险

### 4. GitHub 风格 callout 在 VitePress 下失效（一致性 bug）
**证据**：
- `docs/guide/introduce/平台配置/哔哩哔哩.md` 等页用 `> [!IMPORTANT]` / `> [!WARNING]`
- `docs/.vitepress/theme/index.ts` 仅继承默认主题，无 GitHub alerts 插件；`theme/` 下 grep `alert|markdown-alert` 无匹配
- 对照 `introduce/上手/introduce.md` 用的是 `::: info` / `::: warning`（VitePress 原生容器）

**影响**：`> [!xxx]` 在 VitePress 里只是普通 blockquote，没有彩色 callout 样式；全站 callout 出现"一套 `:::` 容器、一套 `> [!]` 引用"的分裂观感。

**建议**：统一为一种。推荐全站改用 VitePress 原生 `::: info / warning / danger / tip`（零依赖），把平台页的 `> [!xxx]` 批量替换。

### 5. DOCS_STRUCTURE.md 严重过时，多处与真实结构矛盾
这是目前最伤团队信任的一点——新贡献者照它操作会直接写错。

**证据（文档说 vs 实际）**：
- 说"首页是 `introduce/introduce/introduce.md`" → 实际站点首页是 `docs/index.md`（`layout: home`），指引页是 `introduce/上手/introduce.md`
- 说首页有"工作原理"区块（`.arch-flow`） → 实际指引页已无此区块
- 目录树写 `live/`、`基础配置/`、`Config/` → 实际已 rename 为 `平台配置/`、`配置/` 等（`reorganize.py` 已改）
- 路由示例路径还是 `introduce/Config/GlobalConfig`、`introduce/introduce/introduce`
- `base` 写 `/biliup-docs/` → 实际 `/`

**影响**：新贡献者按此文档加页面、写 mapping、数 `../` 都会出错，直接制造死链和错位。

**建议**：以重组后的真实结构重写；或更好——把"新增页面标准流程"浓缩进 `CONTRIBUTING.md`，**删掉易过时的目录树章节**（目录树会随每次改动漂移，本就是维护负担，符合"会漂的别手写"原则）。

### 6. 侧边栏顺序由 mapping.json 隐式决定，平台分组排序混乱
**证据**：`set_sidebar.mts` 用 `Object.keys(nameMappings)`（mapping.json 的 key 顺序）排序；`mapping.json` 里平台配置顺序为：
`acfun, afreecaTV, flextv, nico, twitch, youtube, YY语音, 克拉克拉, 哔哩哔哩, 快手, 斗鱼, 映客, 猫耳FM, 网易CC, 虎牙, 抖音…`

**影响**：既非拼音、非字母、非重要度。抖音（国内大平台）排在第 16 位垫底，用户找平台费劲。

**建议**：在 `mapping.json` 里按"国内大平台优先 + 拼音/字母"重排平台顺序；或给"平台配置"分组单独定义 sortOrder。

### 7. 侧边栏默认全折叠
**证据**：`config.mts` 所有 `set_sidebar(path, false, true)` 第三参 `collapsed=true`

**影响**：从首页进入后侧边栏一片空白，需逐层点开，降低内容可发现性。

**建议**：顶层分组默认展开（`collapsed=false`），至少"指引 / 安装部署"展开。

---

## P2 — 整洁项，有空再做

### 8. 一次性重组脚本硬编码个人绝对路径并入库
**证据**：`reorganize.py:4` `REPO = r"C:/Users/77281/Desktop/文档站/biliup-docs"`；`git ls-files` 显示 `reorganize.py` / `preview_server.py` / `GenerateMapping.ps1` 均被追踪。

**影响**：他人 clone 后这些脚本无意义甚至有风险（会去动你本地路径）；仓库不整洁。

**建议**：删除 `reorganize.py`（已执行完的一次性脚本）；`preview_server.py` 移入 `scripts/` 或直接删除（`npm run docs:preview` 已够用）；`GenerateMapping.ps1` 可保留但移入 `scripts/`。

### 9. editLink 关闭
**证据**：`config.mts:28` `editLink: false`

**建议**：开启并指向仓库，降低社区/团队贡献门槛。

### 10. 平台配置页数量多（20+），部分可能内容稀薄
**建议**：抽查 `afreecaTV` / `Bigo` / `nico` 等海外小平台页，统一模板；过薄的考虑合并进一个"其他平台"索引页，避免侧边栏"长但空"。

### 11. 免责声明语气不一致
**证据**：`introduce/上手/introduce.md` 顶部中性"文档更新可能不及时，以 biliup 主仓库实际代码为准"；`哔哩哔哩.md:84` 写"以下内容如果你不知道是做什么的，那么就不需要修改，**也不要自作聪明的修改**"——带训诫口吻。

**建议**：全站语气统一为中性事实陈述（团队文档约束）。

### 12. changelog 数据准确性
**证据**：`changelog.md` 部分版本只有"具体变更请查看对比链接"无实质内容；`v1.2.0` 发布时间写 `2024-05-31`，而 `v1.2.1` 是 `2026-06-05`，时间线跳跃，疑似日期写错。

**建议**：核对 `v1.2.0` 真实日期；近 N 个版本保留详情，更早的折叠或外链 GitHub Releases。

### 13. title 大小写 "BiliuP" vs 仓库 "biliup"
**证据**：`config.mts` title `BiliuP`；仓库名 `biliup`。

**建议**：确认是否为有意品牌写法，全站统一，避免搜索/品牌混乱。

---

## 已经做对的（保持）

- 顶部"以源码为准"的中性声明（团队文档约束）✓
- 本地搜索（`search.provider: "local"`）✓
- `lastUpdated: true` ✓
- 构建产物 `dist/` `cache/` 已在 `.gitignore` ✓
- CI 完整（checkout → build → upload → deploy）✓
- 首页指引页设计精致、视觉语言统一 ✓
- `rest-api.md` 已瘦身为"索引 + 上游源码链接 + 稳定集成要点 + 使用示例"（见之前讨论）✓

---

## 行动清单（按优先级）

**P0**
- [ ] 修正 `package.json` 元数据（name/repository/author/description）
- [ ] 关闭 `ignoreDeadLinks`，恢复死链检查（先扫存量）
- [ ] 确认部署域名，修正 `base` 与 `CNAME` 矛盾

**P1**
- [ ] 统一 callout 语法为 `:::` 容器
- [ ] 重写或精简 `DOCS_STRUCTURE.md`（删目录树章节，流程进 CONTRIBUTING）
- [ ] 重排 `mapping.json` 平台顺序
- [ ] 侧边栏顶层分组默认展开

**P2**
- [ ] 清掉 `reorganize.py`、归置 `preview_server.py` / `GenerateMapping.ps1`
- [ ] 开启 `editLink`
- [ ] 抽查并统一平台配置页模板
- [ ] 统一免责声明语气
- [ ] 核对 changelog 日期
- [ ] 统一品牌名大小写
