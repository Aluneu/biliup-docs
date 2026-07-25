import mdItCustomAttrs from "markdown-it-custom-attrs";
import { defineConfig } from "vitepress";
import { set_sidebar } from "../guide/set_sidebar.mjs";

export default defineConfig({
  base: "/",
  title: "BiliuP",
  lang: "zh-CN",
  description: "高性能直播录制与视频投稿工具 - CLI + WebUI 交互",
  head: [
    ["meta", { name: "author", content: "BiliuP" }],
    ["meta", { name: "keywords", content: "biliup,直播录制,B站投稿,录播,上传,自动投稿" }],
    ["link", { rel: "icon", href: "/favicon.ico" }],
  ],
  markdown: {
    mermaid: true,
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
      copyright: "Copyright © BiliuP"
    },
    nav: [
      { text: "指引", link: "/guide/getting-started/上手/", activeMatch: "/guide/getting-started/" },
      { text: "WebUI", link: "/guide/webui/usage", activeMatch: "/guide/webui/" },
      { text: "文档", link: "/guide/docs/doc", activeMatch: "/guide/docs/" },
      { text: "API", link: "/guide/api/rest-api", activeMatch: "/guide/api/" },
      { text: "CLI", link: "/guide/configs/config", activeMatch: "/guide/configs/" },
      { text: "Skill", link: "/guide/skill/", activeMatch: "/guide/skill/" },
      { text: "开发", link: "/guide/开发指南/", activeMatch: "/guide/开发指南/" },
      { text: "更新日志", link: "/guide/changelog/changelog", activeMatch: "/guide/changelog/" },
      {
        text: "相关链接",
        items: [
          { text: "GitHub 仓库", link: "https://github.com/biliup/biliup" },
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
      "/guide/开发指南/": set_sidebar('/guide/开发指南', false, false),
    }
  },
  vite: { plugins: [] }
});
