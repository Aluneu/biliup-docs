import mdItCustomAttrs from "markdown-it-custom-attrs";
import { defineConfig } from "vitepress";
import { set_sidebar } from "../guide/set_sidebar.mjs";

export default defineConfig({
  base: "/biliup-docs/",
  title: "BiliuP",
  lang: "zh-CN",
  description: "高性能直播录制与视频投稿工具 - CLI + WebUI 交互",
  head: [
    ["meta", { name: "author", content: "BiliuP" }],
    ["meta", { name: "keywords", content: "biliup,直播录制,B站投稿,录播,上传,自动投稿" }],
    ["link", { rel: "icon", href: "/favicon.ico" }],
  ],
  markdown: { config: (md) => md.use(mdItCustomAttrs, "image", { "data-fancybox": "gallery" }) },
  ignoreDeadLinks: true,
  lastUpdated: true,
  themeConfig: {
    logo: "/icon.png",
    search: { provider: "local" },
    outline: { level: [2, 4], label: '当前页大纲' },
    editLink: false,
    socialLinks: [{ icon: "github", link: "https://github.com/biliup/biliup" }],
    footer: {
      message: "基于 Rust + Python + Next.js 构建",
      copyright: "Copyright © BiliuP"
    },
    nav: [
      { text: "指引", link: "/guide/introduce/introduce/introduce", activeMatch: "/guide/introduce/" },
      { text: "文档", link: "/guide/docs/doc", activeMatch: "/guide/docs/" },
      { text: "CLI", link: "/guide/configs/config", activeMatch: "/guide/configs/" },
      {
        text: "相关链接",
        items: [
          { text: "GitHub 仓库", link: "https://github.com/biliup/biliup" },
          { text: "biliup 社区", link: "https://biliup.me" }
        ]
      },
      // 已删除赞助导航项 // [!code --]
      // { text: "🍵 赞助", link: "/sponsor/index" }, // [!code --]
    ],
    sidebar: {
      "/guide/introduce/": set_sidebar('/guide/introduce', false),
      "/guide/introduce/Config/": set_sidebar('/guide/introduce/Config', false),
      "/guide/introduce/live/": set_sidebar('/guide/introduce/live', false),
      "/guide/docs/": set_sidebar('/guide/docs', false),
      "/guide/configs/": set_sidebar('/guide/configs', false),
      "/guide/webui/": set_sidebar('/guide/webui', false),
      "/guide/api/": set_sidebar('/guide/api', false),
      "/guide/changelog/": set_sidebar('/guide/changelog', false),
    }
  },
  vite: { plugins: [] }
});
