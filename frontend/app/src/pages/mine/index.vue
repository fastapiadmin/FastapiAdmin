<!-- layout: tabbar -->
<script lang="ts" setup>
definePage({
  name: 'mine',
  layout: 'tabbar',
  style: {
    navigationBarTitleText: '我的',
  },
})

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)
const isLogin = computed(() => !!userInfo.value)
const defaultAvatar = '/static/images/default-avatar.png'
const isLoading = ref(false)

// 退出登录
function handleLogout() {
  uni.showModal({
    title: '提示',
    content: '确认退出登录吗？',
    success(res) {
      if (res.confirm) {
        userStore.logout()
        toast.show('已退出登录')
      }
    },
  })
}

// 页面跳转方法
function navigateTo(name: string) {
  router.push({
    name,
  })
}

function openUrl(url: string) {
  window.open(url, '_blank')
}

// 消息按钮点击处理
function handleMessagesClick(e?: any) {
  if (e) {
    e.stopPropagation()
    e.preventDefault()
  }
  navigateToSection('messages')
}

// 导航到各个板块
function navigateToSection(section: string, subSection?: string, e?: any) {
  if (e) {
    e.stopPropagation()
    e.preventDefault()
  }
  // 这里可以根据需要实现具体的导航逻辑
  uni.showToast({
    title: '功能开发中',
    icon: 'none',
  })
}

onShow(() => {
  // 确保 tabbar 状态正确
  const pages = getCurrentPages()
  if (pages.length > 0) {
    const currentPage = pages[pages.length - 1]
    if (currentPage.route === 'pages/mine/index') {
      // 通过事件通知 tabbar 布局更新状态
      uni.$emit('updateTabbar', 'mine')
    }
  }

  // 每次显示页面时都检查并刷新用户信息
  loadUserInfo()
})

// 加载用户信息
async function loadUserInfo() {
  if (isLogin.value) {
    isLoading.value = true
    try {
      await userStore.getInfo()
    }
    catch (error) {
      console.error('获取用户信息失败', error)
    }
    finally {
      isLoading.value = false
    }
  }
}

// 监听用户信息变化，确保数据及时更新
watch(
  () => userInfo.value,
  () => {},
  {
    deep: true,
    immediate: true,
  },
)
</script>

<template>
  <view class="p-3">
    <!-- 用户信息卡片 -->
    <wd-card type="rectangle">
      <wd-row class="flex items-center">
        <wd-col :span="6">
          <wd-badge v-if="true" model-value="99+" @click="handleMessagesClick">
            <wd-avatar
              size="medium"
              shape="round"
              :src="isLogin ? userInfo!.avatar : defaultAvatar"
            />
          </wd-badge>
        </wd-col>
        <wd-col :span="16">
          <view class="mt-2 flex flex-col">
            <wd-text type="success" :text="userInfo?.name || '匿名用户'" size="16" bold />
            <wd-text :text="`ID: ${userInfo?.username}`" size="12" />
          </view>
        </wd-col>
        <wd-col :span="2">
          <wd-icon name="setting" size="22" color="#0083ff" @click="navigateTo('settings')" />
        </wd-col>
      </wd-row>
    </wd-card>

    <!-- 常用工具 -->
    <wd-card type="rectangle" title="常用工具">
      <wd-grid clickable border :gutter="10" :column="4">
        <wd-grid-item is-dot icon="user" text="用户管理" clickable @click="navigateTo('user')" />
        <wd-grid-item is-dot icon="help-circle" text="岗位管理" clickable @click="navigateTo('position')" />
        <wd-grid-item is-dot icon="check-circle" text="角色管理" clickable @click="navigateTo('role')" />
        <wd-grid-item is-dot icon="info-circle" text="参数管理" clickable @click="navigateTo('parameter')" />
        <wd-grid-item is-dot icon="user" text="字典管理" clickable @click="navigateTo('dictionary')" />
        <wd-grid-item is-dot icon="help-circle" text="部门管理" clickable @click="navigateTo('department')" />
        <wd-grid-item is-dot icon="check-circle" text="菜单管理" clickable @click="navigateTo('role')" />
        <wd-grid-item is-dot icon="info-circle" text="日志管理" clickable @click="navigateTo('log')" />
      </wd-grid>
    </wd-card>

    <!-- 推荐服务 -->
    <wd-card type="rectangle" title="推荐服务">
      <wd-cell-group border custom-class="rounded-2! overflow-hidden">
        <wd-cell title="项目官网" is-link @click="openUrl('https://service.fastapiadmin.com/')" />
        <wd-cell title="问题反馈" is-link @click="navigateTo('feedback')" />
        <wd-cell title="个人资料" is-link @click="navigateTo('profile')" />
        <wd-cell title="账号设置" is-link @click="navigateTo('account')" />
      </wd-cell-group>
    </wd-card>

    <!-- 退出登录按钮 -->
    <wd-button v-if="isLogin" class="p-3" size="large" block @click="handleLogout">
      退出登录
    </wd-button>
  </view>
</template>

<style lang="scss" scoped>

</style>
