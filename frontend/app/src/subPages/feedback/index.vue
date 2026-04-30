<script setup lang="ts">
definePage({
  name: 'feedback',
  style: {
    navigationBarTitleText: '全局反馈',
  },
})

const { success: showSuccess } = useGlobalToast()
const { show: showToast, success, error, warning, info } = useGlobalToast()
const { loading, close: closeLoading } = useGlobalLoading()
const { confirm, alert, prompt } = useGlobalMessage()

// 表单数据
const customMessage = ref('这是一个自定义消息')
const loadingText = ref('正在处理中...')

// Toast 演示方法
function demoToastSuccess() {
  success({ msg: '操作成功！' })
}

function demoToastError() {
  error({ msg: '操作失败！' })
}

function demoToastWarning() {
  warning({ msg: '警告提示！' })
}

function demoToastInfo() {
  info({ msg: '信息提示！' })
}

function demoCustomToast() {
  if (!customMessage.value.trim()) {
    warning({ msg: '请输入自定义消息' })
    return
  }
  showToast({
    msg: customMessage.value,
    duration: 3000,
    position: 'middle',
  })
}

function demoToastPosition(position: 'top' | 'middle' | 'bottom') {
  showToast({
    msg: `显示在${position === 'top' ? '顶部' : position === 'middle' ? '中间' : '底部'}的提示`,
    position,
    duration: 2000,
  })
}

// Loading 演示方法
function demoBasicLoading() {
  loading('加载中...')
  setTimeout(() => {
    closeLoading()
    success({ msg: '加载完成！' })
  }, 3000)
}

function demoCustomLoading() {
  if (!loadingText.value.trim()) {
    warning({ msg: '请输入加载文本' })
    return
  }
  loading({
    msg: loadingText.value,
    cover: true,
  })
  setTimeout(() => {
    closeLoading()
    success({ msg: '自定义加载完成！' })
  }, 2500)
}

function demoLoadingNoCover() {
  loading({
    msg: '无遮罩加载',
    cover: false,
  })
  setTimeout(() => {
    closeLoading()
  }, 2000)
}

// Message 演示方法
function demoConfirm() {
  confirm({
    title: '确认操作',
    msg: '您确定要执行此操作吗？',
    success: (res) => {
      if (res.action === 'confirm') {
        success({ msg: '用户确认了操作' })
      }
      else {
        info({ msg: '用户取消了操作' })
      }
    },
  })
}

function demoAlert() {
  alert({
    title: '重要提醒',
    msg: '这是一个重要的提醒信息，请仔细阅读！',
    success: () => {
      success({ msg: '用户已阅读提醒' })
    },
  })
}

function demoPrompt() {
  prompt({
    title: '输入信息',
    msg: '请输入您的姓名：',
    success: (res) => {
      if (res.action === 'confirm') {
        if (res.value && String(res.value).trim()) {
          success({ msg: `您好，${res.value}！` })
        }
        else {
          warning({ msg: '输入不能为空' })
        }
      }
      else {
        info({ msg: '用户取消了输入' })
      }
    },
  })
}

function demoCustomConfirm() {
  confirm({
    title: '自定义确认',
    msg: '这是一个自定义的确认弹窗，可以配置按钮文字和样式',
    confirmButtonText: '好的',
    cancelButtonText: '算了',
    success: (res) => {
      if (res.action === 'confirm') {
        success({ msg: '点击了"好的"' })
      }
      else {
        info({ msg: '点击了"算了"' })
      }
    },
  })
}

// 组合演示
function demoComplex() {
  loading('准备演示...')

  setTimeout(() => {
    closeLoading()
    confirm({
      title: '组合演示',
      msg: '这是一个组合演示，将依次展示不同的反馈效果。是否继续？',
      success: (res) => {
        if (res.action === 'confirm') {
          success({ msg: '开始演示' })

          setTimeout(() => {
            loading('演示进行中...')

            setTimeout(() => {
              closeLoading()
              info({ msg: '演示完成！' })
            }, 2000)
          }, 1000)
        }
        else {
          info({ msg: '已取消演示' })
        }
      },
    })
  }, 1000)
}

// 代码示例常量
const codeExamples = {
  basicToast: `const { success, error, warning, info } = useGlobalToast()

// 使用方法
success({ msg: '操作成功！' })
error({ msg: '操作失败！' })
warning({ msg: '警告提示！' })
info({ msg: '信息提示！' })`,

  customToast: `const { show } = useGlobalToast()

show({
  msg: '自定义消息',
  duration: 3000,
  position: 'middle' // 'top' | 'middle' | 'bottom'
})`,

  basicLoading: `const { loading, close } = useGlobalLoading()

// 基础用法
loading('加载中...')

// 手动关闭
close()`,

  customLoading: `loading({
  msg: '正在处理中...',
  cover: true // 是否显示遮罩
})`,

  basicMessage: `const { confirm, alert, prompt } = useGlobalMessage()

// 确认弹窗
confirm({
  title: '确认操作',
  msg: '您确定要执行此操作吗？',
  success: (res) => {
    if (res.action === 'confirm') {
      // 用户确认
    }
  }
})`,

  customMessage: `confirm({
  title: '自定义确认',
  msg: '自定义的确认弹窗',
  confirmButtonText: '好的',
  cancelButtonText: '算了',
  success: (res) => {
    // res.action: 'confirm' | 'cancel'
  }
})`,
}

// 复制代码到剪贴板
function copyCode(code: string) {
  uni.setClipboardData({
    data: code,
    showToast: false,
    success: () => {
      uni.hideToast()
      showSuccess({ msg: '代码已复制到剪贴板' })
    },
  })
}

// 链接导航处理
function handleNavigate(url: string) {
  // #ifdef H5
  window.open(url, '_blank')
  // #endif
  // #ifndef H5
  uni.setClipboardData({
    data: url,
    showToast: false,
    success: () => {
      uni.hideToast()
      showSuccess({ msg: `${url} 已复制到剪贴板` })
    },
  })
  // #endif
}
</script>

<template>
  <view class="min-h-screen bg-gray-100 py-3 dark:bg-[var(--wot-dark-background)]">
    <!-- 头部介绍 -->
    <view class="mx-3 mb-3">
      <view class="rounded-3 bg-white px-5 py-8 text-center dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-10">
          💬
        </view>
        <view class="mb-2 text-6 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          全局反馈组件
        </view>
        <view class="mb-2 text-3.5 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          GlobalToast / GlobalLoading / GlobalMessage
        </view>
        <view class="text-3 text-gray-500 dark:text-[var(--wot-dark-color2)]">
          统一的用户反馈交互体验，支持在路由导航守卫和网络请求拦截器中使用，扩展 WotUI 交互组件能力。
        </view>
      </view>
    </view>

    <!-- GlobalToast 演示 -->
    <demo-block title="GlobalToast 轻提示" transparent>
      <view class="space-y-4">
        <!-- 基础用法 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            基础用法
          </view>
          <view class="grid grid-cols-2 mb-3 gap-2">
            <wd-button type="success" size="small" @click="demoToastSuccess">
              成功提示
            </wd-button>
            <wd-button type="error" size="small" @click="demoToastError">
              错误提示
            </wd-button>
            <wd-button type="warning" size="small" @click="demoToastWarning">
              警告提示
            </wd-button>
            <wd-button type="info" size="small" @click="demoToastInfo">
              信息提示
            </wd-button>
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(codeExamples.basicToast)"
          >
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              代码示例:
            </view>
            <view class="whitespace-pre-line text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              const { success, error, warning, info } = useGlobalToast()

              success({ msg: '操作成功！' })
              error({ msg: '操作失败！' })
            </view>
          </view>
        </view>

        <!-- 自定义用法 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            自定义配置
          </view>
          <view class="mb-3">
            <wd-input v-model="customMessage" placeholder="请输入自定义消息" />
          </view>
          <view class="grid grid-cols-2 mb-3 gap-2">
            <wd-button type="primary" size="small" @click="demoCustomToast">
              自定义消息
            </wd-button>
            <wd-button type="success" size="small" @click="demoToastPosition('top')">
              顶部显示
            </wd-button>
            <wd-button type="warning" size="small" @click="demoToastPosition('middle')">
              中间显示
            </wd-button>
            <wd-button type="info" size="small" @click="demoToastPosition('bottom')">
              底部显示
            </wd-button>
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(codeExamples.customToast)"
          >
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              自定义配置:
            </view>
            <view class="whitespace-pre-line text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              show({
              msg: '自定义消息',
              duration: 3000,
              position: 'middle'
              })
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- GlobalLoading 演示 -->
    <demo-block title="GlobalLoading 加载提示" transparent>
      <view class="space-y-4">
        <!-- 基础用法 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            基础用法
          </view>
          <view class="grid grid-cols-2 mb-3 gap-2">
            <wd-button type="primary" size="small" @click="demoBasicLoading">
              显示加载(3秒)
            </wd-button>
            <wd-button type="warning" size="small" @click="closeLoading">
              手动关闭
            </wd-button>
            <wd-button type="success" size="small" @click="demoLoadingNoCover">
              无遮罩加载
            </wd-button>
            <wd-button type="info" size="small" @click="demoComplex">
              组合演示
            </wd-button>
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(codeExamples.basicLoading)"
          >
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              代码示例:
            </view>
            <view class="whitespace-pre-line text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              const { loading, close } = useGlobalLoading()

              loading('加载中...')
              close()
            </view>
          </view>
        </view>

        <!-- 自定义用法 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            自定义配置
          </view>
          <view class="mb-3">
            <wd-input v-model="loadingText" placeholder="请输入加载文本" />
          </view>
          <view class="mb-3">
            <wd-button type="primary" block @click="demoCustomLoading">
              自定义加载文本
            </wd-button>
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(codeExamples.customLoading)"
          >
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              自定义配置:
            </view>
            <view class="whitespace-pre-line text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              loading({
              msg: '正在处理中...',
              cover: true // 是否显示遮罩
              })
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- GlobalMessage 演示 -->
    <demo-block title="GlobalMessage 弹窗提示" transparent>
      <view class="space-y-4">
        <!-- 基础用法 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            基础用法
          </view>
          <view class="grid grid-cols-3 mb-3 gap-2">
            <wd-button type="primary" size="small" @click="demoConfirm">
              确认弹窗
            </wd-button>
            <wd-button type="warning" size="small" @click="demoAlert">
              警告弹窗
            </wd-button>
            <wd-button type="success" size="small" @click="demoPrompt">
              输入弹窗
            </wd-button>
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(codeExamples.basicMessage)"
          >
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              代码示例:
            </view>
            <view class="whitespace-pre-line text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              confirm({
              title: '确认操作',
              msg: '您确定要执行此操作吗？',
              success: (res) => { /* 处理结果 */ }
              })
            </view>
          </view>
        </view>

        <!-- 自定义用法 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            自定义配置
          </view>
          <view class="mb-3">
            <wd-button type="primary" block @click="demoCustomConfirm">
              自定义按钮文字
            </wd-button>
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(codeExamples.customMessage)"
          >
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              自定义按钮:
            </view>
            <view class="whitespace-pre-line text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              confirm({
              confirmButtonText: '好的',
              cancelButtonText: '算了'
              })
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 组件特性 -->
    <demo-block title="组件特性" transparent>
      <view class="space-y-3">
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 flex items-center">
            <view class="mr-2 text-6">
              🎯
            </view>
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              设计理念
            </view>
          </view>
          <view class="text-3 text-gray-600 leading-relaxed space-y-2 dark:text-[var(--wot-dark-color2)]">
            <view>
              • <text class="text-blue-600 font-bold dark:text-blue-400">
                全局单例
              </text>：整个应用只有一个实例，避免重复创建
            </view>
            <view>
              • <text class="text-green-600 font-bold dark:text-green-400">
                状态管理
              </text>：基于 Pinia 管理组件状态，响应式更新
            </view>
            <view>
              • <text class="text-purple-600 font-bold dark:text-purple-400">
                类型安全
              </text>：完整的 TypeScript 类型定义
            </view>
            <view>
              • <text class="text-orange-600 font-bold dark:text-orange-400">
                易于使用
              </text>：简洁的 API 设计，开箱即用
            </view>
          </view>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 flex items-center">
            <view class="mr-2 text-6">
              ⚡
            </view>
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              使用优势
            </view>
          </view>
          <view class="text-3 text-gray-600 leading-relaxed space-y-2 dark:text-[var(--wot-dark-color2)]">
            <view>• 统一的用户反馈体验</view>
            <view>• 避免组件重复创建和销毁</view>
            <view>• 支持深色模式自动适配</view>
            <view>• 可在任意组件中调用</view>
          </view>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 flex items-center">
            <view class="mr-2 text-6">
              📝
            </view>
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              最佳实践
            </view>
          </view>
          <view class="text-3 text-gray-600 leading-relaxed space-y-2 dark:text-[var(--wot-dark-color2)]">
            <view>• Toast：用于简短的状态反馈，不打断用户操作</view>
            <view>• Loading：用于异步操作的等待提示</view>
            <view>• Message：用于重要信息确认和用户输入</view>
            <view>• 合理控制显示时长，避免信息过载</view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 相关链接 -->
    <demo-block title="相关链接" transparent>
      <wd-cell-group border custom-class="rounded-2! overflow-hidden">
        <wd-cell title="📚 WotUI Toast" value="轻提示组件" is-link @click="handleNavigate('https://wot-ui.cn/component/toast.html')" />
        <wd-cell title="🔄 WotUI Loading" value="加载组件" is-link @click="handleNavigate('https://wot-ui.cn/component/loading.html')" />
        <wd-cell title="💬 WotUI MessageBox" value="弹窗组件" is-link @click="handleNavigate('https://wot-ui.cn/component/message-box.html')" />
        <wd-cell title="🍍 Pinia 状态管理" value="Vue 状态库" is-link @click="handleNavigate('https://pinia.vuejs.org/zh/')" />
      </wd-cell-group>
    </demo-block>
  </view>
</template>
