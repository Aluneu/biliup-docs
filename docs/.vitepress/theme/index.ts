// biliup 主题入口 - 基于 VitePress 默认主题扩展
import DefaultTheme from 'vitepress/theme'
import './custom.css'
import WorkflowDiagram from '../components/WorkflowDiagram.vue'
import Layout from './Layout.vue'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp(ctx) {
    DefaultTheme.enhanceApp(ctx)
    ctx.app.component('WorkflowDiagram', WorkflowDiagram)
  }
}
