import mdItCustomAttrs from "markdown-it-custom-attrs";
import { defineConfig } from "vitepress";
import { set_sidebar } from "../guide/set_sidebar.mts";

export default defineConfig({
  base: "/",
  title: "biliup",
  titleTemplate: ":title · biliup 文档",
  lang: "zh-CN",
  description: "高性能直播录制与视频投稿工具 - CLI + WebUI 交互",
  sitemap: { hostname: "https://doc.biliup.rs" },
  head: [
    ["meta", { name: "author", content: "biliup" }],
    ["meta", { name: "keywords", content: "biliup,直播录制,B站投稿,录播,上传,自动投稿,直播录制工具" }],
    ["meta", { name: "theme-color", content: "#1890ff" }],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:site_name", content: "biliup 文档" }],
    ["meta", { property: "og:locale", content: "zh_CN" }],
    ["meta", { property: "og:image", content: "https://doc.biliup.rs/home.webp" }],
    ["meta", { name: "twitter:card", content: "summary_large_image" }],
    ["meta", { name: "twitter:image", content: "https://doc.biliup.rs/home.webp" }],
    ["link", { rel: "icon", href: "/favicon.ico" }],
    ["link", { rel: "apple-touch-icon", href: "/icon.png" }],
  ],
  transformHead({ pageData }) {
    const rel = pageData.relativePath.replace(/index\.md$/, "").replace(/\.md$/, ".html");
    const url = `https://doc.biliup.rs/${rel.split("/").map(encodeURIComponent).join("/")}`;
    const desc = pageData.frontmatter.description || pageData.description;
    const tags = [
      ["link", { rel: "canonical", href: url }],
      ["meta", { property: "og:url", content: url }],
      ["meta", { property: "og:title", content: pageData.title ? `${pageData.title} · biliup 文档` : "biliup 文档" }],
    ];
    if (desc) {
      tags.push(["meta", { property: "og:description", content: desc }]);
      tags.push(["meta", { name: "twitter:description", content: desc }]);
    }
    return tags;
  },
  markdown: {
    mermaid: true,
    // Caddyfile 不在 shiki 预置语言内，映射到 nginx 以获得可用的指令高亮
    languageAlias: { caddyfile: "nginx" },
    config: (md) => md.use(mdItCustomAttrs, "image", { "data-fancybox": "gallery" }),
  },
  lastUpdated: true,
  themeConfig: {
    logo: "/icon.png",
    search: { provider: "local" },
    outline: { level: [2, 4], label: '当前页大纲' },
    editLink: {
      pattern: 'https://github.com/Aluneu/biliup-docs/edit/main/docs/:path',
      text: '编辑此页'
    },
    socialLinks: [{ icon: "github", link: "https://github.com/biliup/biliup" }],
    footer: {
      message: "基于 Rust + Python + Next.js 构建",
      copyright: "Copyright © biliup"
    },
    nav: [
      { text: "指引", link: "/guide/getting-started/上手/", activeMatch: "/guide/getting-started/" },
      { text: "工作原理", link: "/guide/workflow-demo/", activeMatch: "/guide/workflow-demo/" },
      { text: "教程", link: "/guide/tutorials/recording-and-masking", activeMatch: "/guide/tutorials/" },
      { text: "WebUI", link: "/guide/webui/usage", activeMatch: "/guide/webui/" },
      { text: "API", link: "/guide/api/rest-api", activeMatch: "/guide/api/" },
      { text: "命令行", link: "/guide/configs/config", activeMatch: "/guide/configs/" },
      { text: "Skill", link: "/guide/skill/", activeMatch: "/guide/skill/" },
      { text: "开发", link: "/guide/开发指南/", activeMatch: "/guide/开发指南/" },
      { text: "更新日志", link: "/guide/changelog/changelog", activeMatch: "/guide/changelog/" },
      {
        text: "相关链接",
        items: [
          { text: "GitHub 仓库", link: "https://github.com/biliup/biliup" },
          { text: "论坛 BBS", link: "https://bbs.biliup.rs" },
          { text: "biliup 社区", link: "https://biliup.me" }
        ]
      },
      { text: "🍵 赞助", link: "/sponsor/index" },
    ],
    sidebar: {
      "/guide/getting-started/": set_sidebar('/guide/getting-started', false, false),      "/guide/docs/": set_sidebar('/guide/docs', false, false),
      "/guide/configs/": set_sidebar('/guide/configs', false, false),      "/guide/webui/": set_sidebar('/guide/webui', false, false),
      "/guide/api/": set_sidebar('/guide/api', false, false),
      "/guide/changelog/": set_sidebar('/guide/changelog', false, false),
      "/guide/skill/": set_sidebar('/guide/skill', false, false),
      "/guide/workflow-demo/": set_sidebar('/guide/workflow-demo', false, false),
      "/guide/tutorials/": set_sidebar('/guide/tutorials', false, false),
      "/guide/开发指南/": set_sidebar('/guide/开发指南', false, false),
    }
  },
  vite: { plugins: [] }
});
