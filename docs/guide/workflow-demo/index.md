---
title: biliup 工作流程（演示页）
---

# biliup 工作流程

> 本页为演示页，未加入侧边栏导航，仅供预览树状图效果（纯 HTML/CSS 实现，不依赖 Mermaid 插件）。

<style>
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
</style>

<div class="wf-tree">
  <div class="wf-root"><div class="box">biliup<br>工作流程</div></div>
  <div class="wf-spine"></div>
  <div class="wf-branches">

    <div class="wf-branch">
      <div class="wf-cat c1">素材获取</div>
      <div class="wf-items">
        <span class="wf-item">直播链路</span>
        <span class="wf-item">本地链路</span>
      </div>
    </div>

    <div class="wf-branch">
      <div class="wf-cat c2">媒体预处理</div>
      <div class="wf-items">
        <span class="wf-item">FFmpeg 转码压缩</span>
        <span class="wf-item">封面、字幕处理</span>
        <span class="wf-item">文件完整性校验</span>
      </div>
    </div>

    <div class="wf-branch">
      <div class="wf-cat c3">B站鉴权</div>
      <div class="wf-items">
        <span class="wf-item">读取本地登录凭证</span>
        <span class="wf-item">凭证失效终止任务</span>
      </div>
    </div>

    <div class="wf-branch">
      <div class="wf-cat c4">分片上传调度</div>
      <div class="wf-items">
        <span class="wf-item">任务队列限流排队</span>
        <span class="wf-item">文件分片上传</span>
        <span class="wf-item">断点续传</span>
        <span class="wf-item">分片合并请求</span>
      </div>
    </div>

    <div class="wf-branch">
      <div class="wf-cat c5">稿件提交</div>
      <div class="wf-items">
        <span class="wf-item">填充投稿参数</span>
        <span class="wf-item">调用稿件审核接口</span>
      </div>
    </div>

    <div class="wf-branch">
      <div class="wf-cat c6">运行容错机制</div>
      <div class="wf-items">
        <span class="wf-item">录制断线重连</span>
        <span class="wf-item">接口报错自动重试</span>
        <span class="wf-item">全流程日志记录</span>
      </div>
    </div>

    <div class="wf-branch">
      <div class="wf-cat c7">任务收尾</div>
      <div class="wf-items">
        <span class="wf-item">记录上传状态</span>
        <span class="wf-item">可选自动归档本地视频</span>
      </div>
    </div>

  </div>
</div>
