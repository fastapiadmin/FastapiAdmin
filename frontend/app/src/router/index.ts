/// <reference types="@uni-helper/vite-plugin-uni-pages/client" />
import { pages, subPackages } from 'virtual:uni-pages'
import { useUserStore } from '@/store/userStore'

function generateRoutes() {
  const routes = pages.map((page) => {
    const newPath = `/${page.path}`
    return { ...page, path: newPath }
  })
  if (subPackages && subPackages.length > 0) {
    subPackages.forEach((subPackage) => {
      const subRoutes = subPackage.pages.map((page: any) => {
        const newPath = `/${subPackage.root}/${page.path}`
        return { ...page, path: newPath }
      })
      routes.push(...subRoutes)
    })
  }
  return routes
}

const router = createRouter({
  routes: generateRoutes(),
})
router.beforeEach((to, from, next) => {
  console.log('🚀 beforeEach 守卫触发:', { to, from })

  // 演示：基本的导航日志记录
  if (to.path && from.path) {
    console.log(`📍 导航: ${from.path} → ${to.path}`)
  }

  // 跳过登录页面的检查
  if (to.path === '/pages/login/index') {
    return next()
  }

  // 检查登录状态
  try {
    const userStore = useUserStore()
    const accessToken = userStore.getAccessToken()

    if (!accessToken) {
      uni.showToast({
        title: '🔐 Token不存在，跳转到登录页面',
        icon: 'error',
      })
      // 跳转到登录页面
      uni.navigateTo({
        url: `/pages/login/index?redirect=${encodeURIComponent(to.path)}`,
        fail: (error) => {
          console.error('跳转登录页面失败:', error)
          // 如果 navigateTo 失败，尝试使用 reLaunch
          uni.reLaunch({
            url: '/pages/login/index',
          })
        },
      })
      return
    }
  }
  catch (error) {
    console.error('检查登录状态时发生错误:', error)
    // 发生错误时，跳转到登录页面
    uni.reLaunch({
      url: '/pages/login/index',
    })
    return
  }

  // 演示：对受保护页面的简单拦截
  if (to.name === 'demo-protected') {
    const { confirm: showConfirm } = useGlobalMessage()
    console.log('🛡️ 检测到访问受保护页面')

    return new Promise<void>((resolve, reject) => {
      showConfirm({
        title: '守卫拦截演示',
        msg: '这是一个受保护的页面，需要确认后才能访问',
        confirmButtonText: '允许访问',
        cancelButtonText: '取消',
        success() {
          console.log('✅ 用户确认访问，允许导航')
          next()
          resolve()
        },
        fail() {
          console.log('❌ 用户取消访问，阻止导航')
          next(false)
          reject(new Error('用户取消访问'))
        },
      })
    })
  }

  // 继续导航
  next()
})

router.afterEach((to, from) => {
  console.log('🎯 afterEach 钩子触发:', { to, from })

  // 演示：简单的页面切换记录
  if (to.path) {
    console.log(`📄 页面切换完成: ${to.path}`)
  }

  // 演示：针对 afterEach 演示页面的简单提示
  if (to.name === 'demo-aftereach') {
    const { show: showToast } = useGlobalToast()
    console.log('📊 进入 afterEach 演示页面')
    setTimeout(() => {
      showToast('afterEach 钩子已触发！')
    }, 500)
  }
})

export default router
