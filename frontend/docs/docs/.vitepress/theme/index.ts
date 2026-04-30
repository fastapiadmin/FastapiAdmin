import Theme from 'vitepress/theme'
import { onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'
import mediumZoom from 'medium-zoom'
import './style.css'

export default {
  ...Theme,
  setup() {
    const route = useRoute()
    let zoom: ReturnType<typeof mediumZoom> | null = null

    const initZoom = () => {
      // 销毁之前的实例
      if (zoom) {
        zoom.detach()
      }
      
      // 等待 DOM 更新后初始化
      nextTick(() => {
        // 初始化图片放大功能
        // 选择所有文章内容中的图片，排除 logo、badge 等装饰性图片
        zoom = mediumZoom('.vp-doc img:not(.logo):not([alt*="badge"]):not([alt*="Badge"]):not([alt*="Stars"]):not([alt*="License"]):not([alt*="Python"]):not([alt*="NodeJS"]):not([alt*="MySQL"]):not([alt*="Redis"])', {
          background: 'rgba(0, 0, 0, 0.8)',
          margin: 24,
          scrollOffset: 0,
        })
      })
    }

    onMounted(() => {
      initZoom()
      
      // 监听路由变化，重新初始化图片放大功能
      watch(() => route.path, () => {
        initZoom()
      })
    })
  }
}