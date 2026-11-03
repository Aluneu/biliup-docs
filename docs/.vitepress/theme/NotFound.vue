<script setup lang="ts">
import { useData } from 'vitepress'
const { isDark } = useData()
</script>

<template>
  <div class="nf-wrap">
    <div class="nf-card">
      <p class="nf-code">404</p>
      <h1>这一页不存在</h1>
      <p class="nf-text">链接可能写错了，或者文档改版后地址变了。</p>
      <div class="nf-actions">
        <a class="nf-btn" href="/guide/getting-started/上手/">看快速上手</a>
        <a class="nf-btn ghost" href="/">回首页</a>
      </div>
      <p class="nf-hint">
        也可以用右上角搜索：平台名、配置项（如 <code>submit_api</code>）、错误关键词都能搜。
      </p>
    </div>
  </div>
</template>

<style scoped>
.nf-wrap {
  display: flex;
  justify-content: center;
  padding: 10vh 24px 0;
}
.nf-card {
  max-width: 560px;
  text-align: center;
}
.nf-code {
  font-size: 72px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -2px;
  margin: 0;
  color: var(--vp-c-brand-1);
}
h1 {
  font-size: 24px;
  margin: 16px 0 8px;
  border: 0;
}
.nf-text {
  color: var(--vp-c-text-2);
  margin: 0;
}
.nf-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin: 28px 0 20px;
  flex-wrap: wrap;
}
.nf-btn {
  padding: 10px 20px;
  border-radius: 8px;
  background: var(--vp-c-brand-1);
  color: #fff !important;
  font-weight: 600;
  text-decoration: none;
}
.nf-btn:hover {
  background: var(--vp-c-brand-2);
}
.nf-btn.ghost {
  background: transparent;
  color: var(--vp-c-brand-1) !important;
  border: 1px solid var(--vp-c-brand-1);
}
.nf-hint {
  font-size: 13px;
  color: var(--vp-c-text-3);
}
</style>
