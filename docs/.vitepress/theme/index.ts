// BiliuP 主题入口 - 基于 VitePress 默认主题扩展
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp(ctx) {
    DefaultTheme.enhanceApp(ctx)
  }
}
