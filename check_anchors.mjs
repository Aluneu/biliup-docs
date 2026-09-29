#!/usr/bin/env node
/**
 * 站内链接锚点校验
 *
 * VitePress 的死链检查（构建时的 dead link 检测）只校验文件是否存在，
 * **不校验 `#锚点` 是否真的存在**。锚点写错时链接不会报错，但点击后
 * 只会停在目标页顶部，静默失效。这个脚本补上这一环。
 *
 * 用法（在仓库根目录执行）：
 *   node check_anchors.mjs
 *   npm run docs:check-anchors
 *
 * 有失效锚点时以非 0 退出码结束，可直接用于 CI 或 pre-commit。
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = path.dirname(fileURLToPath(import.meta.url));
const DOCS = path.join(REPO, "docs");
const SKIP_DIRS = new Set([".vitepress", "node_modules", ".git", "dist", ".temp"]);

// 与 @mdit-vue/plugin-headers 的 slugify 保持一致。
// 关键点：特殊字符是**替换为 `-`**，不是删除；中文标点（：（）等）同样计入，
// 且已经出现的 `-` 也会参与替换。
const rControl = /[\u0000-\u001f]/g;
const rSpecial = /[\s~`!@#$%^&*()\-_+=[\]{}|\\;:"'\u201c\u201d\u2018\u2019<>,.?/]+/g;
const rCombining = /[\u0300-\u036F]/g;

const slugify = (str) =>
  str
    .normalize("NFKD")
    .replace(rCombining, "")
    .replace(rControl, "")
    .replace(rSpecial, "-")
    .replace(/-{2,}/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/^(\d)/, "_$1")
    .toLowerCase();

function walk(dir, acc = []) {
  for (const entry of fs.readdirSync(dir)) {
    const full = path.join(dir, entry);
    if (fs.statSync(full).isDirectory()) {
      if (SKIP_DIRS.has(entry)) continue;
      walk(full, acc);
    } else if (entry.endsWith(".md")) {
      acc.push(full);
    }
  }
  return acc;
}

/** 收集每个文档页面的锚点集合（标题 slug + 显式 {#id}） */
function collectAnchors(file) {
  const ids = new Set();
  for (const line of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
    const heading = line.match(/^#{1,6}\s+(.+?)\s*$/);
    if (!heading) continue;
    let title = heading[1].trim();
    const explicit = title.match(/\{#([^}]+)\}\s*$/);
    if (explicit) {
      ids.add(explicit[1]);
      title = title.replace(/\s*\{#([^}]+)\}\s*$/, "").trim();
    }
    ids.add(slugify(title));
  }
  return ids;
}

const rel = (p) => path.relative(REPO, p).split(path.sep).join("/");

const files = walk(DOCS);
const anchors = new Map(files.map((f) => [f, collectAnchors(f)]));

let checked = 0;
const problems = [];

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  // 只看 markdown 链接语法，跳过外链与纯锚点
  for (const match of text.matchAll(/\]\((?!https?:|mailto:)([^)\s]+?)\)/g)) {
    const link = match[1];
    const hashAt = link.indexOf("#");
    if (hashAt === -1) continue;

    const target = decodeURIComponent(link.slice(0, hashAt));
    const anchor = decodeURIComponent(link.slice(hashAt + 1));
    if (!anchor) continue;

    let targetFile;
    if (target.startsWith("/")) {
      targetFile = path.join(DOCS, target);
    } else if (target) {
      targetFile = path.resolve(path.dirname(file), target);
    } else {
      targetFile = file;
    }

    // 目录链接 -> index.md；.html -> .md
    if (targetFile.endsWith(path.sep) || /\/$/.test(targetFile)) {
      targetFile = path.join(targetFile, "index.md");
    }
    if (!targetFile.endsWith(".md")) targetFile = targetFile.replace(/\.html$/, ".md");

    if (!fs.existsSync(targetFile)) {
      problems.push(`[文件缺失] ${rel(file)} -> ${link}`);
      continue;
    }

    checked++;
    if (!anchors.get(targetFile)?.has(anchor)) {
      problems.push(`[锚点失效] ${rel(file)} -> ${link}`);
    }
  }
}

if (problems.length) {
  console.error(problems.join("\n"));
  console.error(`\n检查 ${checked} 个锚点链接，发现 ${problems.length} 处问题。`);
  process.exit(1);
}

console.log(`锚点校验通过：${checked} 个锚点链接全部有效。`);
