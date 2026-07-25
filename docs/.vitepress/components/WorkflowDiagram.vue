<template>
  <div class="wf-tree">
    <div class="wf-root">
      <div class="box">biliup<br>工作流程</div>
    </div>
    <div class="wf-spine"></div>
    <div class="wf-branches">
      <div v-for="branch in branches" :key="branch.cat" class="wf-branch">
        <div class="wf-cat" :class="branch.cls">{{ branch.cat }}</div>
        <div class="wf-items">
          <span v-for="item in branch.items" :key="item" class="wf-item">{{ item }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const branches = [
  { cls: 'c1', cat: '素材获取', items: ['直播链路', '本地链路'] },
  { cls: 'c2', cat: '媒体预处理', items: ['FFmpeg 转码压缩', '封面、字幕处理', '文件完整性校验'] },
  { cls: 'c3', cat: 'B站鉴权', items: ['读取本地登录凭证', '凭证失效终止任务'] },
  { cls: 'c4', cat: '分片上传调度', items: ['任务队列限流排队', '文件分片上传', '断点续传', '分片合并请求'] },
  { cls: 'c5', cat: '稿件提交', items: ['填充投稿参数', '调用稿件审核接口'] },
  { cls: 'c6', cat: '运行容错机制', items: ['录制断线重连', '接口报错自动重试', '全流程日志记录'] },
  { cls: 'c7', cat: '任务收尾', items: ['记录上传状态', '可选自动归档本地视频'] }
]
</script>

<style scoped>
.wf-tree {
  display: flex;
  gap: 0;
  margin: 28px 0;
  font-size: 14px;
}
.wf-root {
  flex: 0 0 130px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.wf-root .box {
  background: linear-gradient(135deg, #6366f1, #fb7299);
  color: #fff;
  font-weight: 700;
  font-size: 15px;
  text-align: center;
  line-height: 1.4;
  padding: 16px 14px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25);
}
.wf-spine {
  flex: 0 0 28px;
  position: relative;
  border-left: 2px solid var(--vp-c-divider);
  margin-left: 6px;
}
.wf-branches {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-left: 6px;
}
.wf-branch {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}
.wf-spine::before {
  content: "";
  position: absolute;
  left: -2px;
  top: 22px;
  width: 14px;
  height: 2px;
  background: var(--vp-c-divider);
}
.wf-cat {
  flex: 0 0 132px;
  font-weight: 600;
  color: var(--vp-c-text-1);
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid transparent;
  text-align: center;
}
.wf-items {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 4px;
}
.wf-item {
  font-size: 13px;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  padding: 5px 12px;
  border-radius: 999px;
}
.c1 { background: #E6F1FB; border-color: #185FA5; color: #103A63; }
.c2 { background: #E1F5EE; border-color: #0F6E56; color: #0A4636; }
.c3 { background: #FAEEDA; border-color: #854F0B; color: #5E3706; }
.c4 { background: #FAECE7; border-color: #993C1D; color: #5E2412; }
.c5 { background: #FBEAF0; border-color: #993556; color: #5E2033; }
.c6 { background: #EAF3DE; border-color: #3B6D11; color: #274A0A; }
.c7 { background: #F1EFE8; border-color: #5F5E5A; color: #3A3935; }
.dark .wf-item { background: rgba(40,40,55,0.5); }
@media (max-width: 640px) {
  .wf-tree { flex-direction: column; }
  .wf-root { flex: none; margin-bottom: 14px; }
  .wf-spine { display: none; }
  .wf-branch { flex-direction: column; gap: 8px; }
  .wf-cat { flex: none; width: fit-content; }
}
</style>
