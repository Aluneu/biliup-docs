// 构建产物死链 / 锚点巡检：先 npm run docs:build，再跑这个。
// VitePress 自带 build 阶段的死链检查只覆盖 .md 源文件里的相对链接；
// 这里扫的是真正生成的 HTML，能抓到 frontmatter、组件里的绝对链接与锚点。
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve('docs/.vitepress/dist')

if (!fs.existsSync(ROOT)) {
  console.error(`找不到构建产物：${ROOT}，先执行 npm run docs:build`)
  process.exit(1)
}

const files = []
;(function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(full)
    else if (entry.name.endsWith('.html')) files.push(full)
  }
})(ROOT)

let checked = 0
let anchors = 0
const broken = []
const badAnchors = []

for (const file of files) {
  const html = fs.readFileSync(file, 'utf8')
  const from = path.relative(ROOT, file).replace(/\\/g, '/')
  for (const match of html.matchAll(/href="(\/[^"#]*\.html)(#[^"]*)?"/g)) {
    const target = decodeURIComponent(match[1])
    const hash = match[2] ? decodeURIComponent(match[2].slice(1)) : null
    const targetPath = path.join(ROOT, target)
    checked++
    if (!fs.existsSync(targetPath)) {
      broken.push(`${from} -> ${match[1]}`)
      continue
    }
    if (hash) {
      anchors++
      const ids = [...fs.readFileSync(targetPath, 'utf8').matchAll(/id="([^"]+)"/g)].map((m) => m[1])
      if (!ids.includes(hash)) badAnchors.push(`${from} -> ${match[1]}#${hash}`)
    }
  }
}

for (const line of broken) console.error(`BROKEN     ${line}`)
for (const line of badAnchors) console.error(`BADANCHOR  ${line}`)

console.log(
  `巡检完成：${files.length} 个页面，${checked} 个站内链接，${anchors} 个锚点；` +
    `死链 ${broken.length}，坏锚点 ${badAnchors.length}`
)

if (broken.length || badAnchors.length) process.exit(1)
