<script setup lang="ts">
definePage({
  name: 'ci',
  style: {
    navigationBarTitleText: 'CI 持续集成',
  },
})

const { success: showSuccess } = useGlobalToast()

// 配置示例数据
const configExample = ref(`{
  "weixin": {
    "appid": "微信小程序appid",
    "privateKeyPath": "key/private.appid.key",
    "projectPath": "dist/build/mp-weixin"
  },
  "alipay": {
    "appid": "支付宝小程序appid",
    "toolId": "支付宝开放平台工具ID",
    "privateKey": "私钥文本内容",
    "projectPath": "dist/build/mp-alipay",
    "autoincrement": true
  },
  "dd": {
    "appid": "钉钉小程序appid",
    "token": "钉钉开发者后台的 API Token",
    "projectPath": "dist/build/mp-alipay",
    "autoincrement": true
  },
  "version": "0.0.1",
  "desc": "版本描述"
}`)

const packageScripts = ref(`{
  "scripts": {
    "upload:weixin": "minici --platform weixin",
    "upload:alipay": "minici --platform alipay",
    "upload:dd": "minici --platform dd",
    "upload:mp-weixin": "uni build -p mp-weixin && minici --platform weixin",
    "upload:mp-alipay": "uni build -p mp-alipay && minici --platform alipay",
    "upload:mp-dingtalk": "uni build -p mp-dingtalk && minici --platform dd"
  }
}`)

// 特性列表
const features = ref([
  {
    icon: '📱',
    title: '多平台支持',
    desc: '支持微信、支付宝、钉钉小程序的上传',
  },
  {
    icon: '🔢',
    title: '版本管理',
    desc: '支持指定版本号和版本号自增',
  },
  {
    icon: '⚙️',
    title: '简单配置',
    desc: '通过配置文件轻松管理多平台参数',
  },
  {
    icon: '🔄',
    title: 'CI/CD集成',
    desc: '完美集成持续集成和持续部署流程',
  },
  {
    icon: '🛠️',
    title: '命令行工具',
    desc: '支持全局和局部安装，灵活使用',
  },
  {
    icon: '📦',
    title: '打包上传',
    desc: '支持打包和上传命令组合使用',
  },
])

// 平台配置
const platforms = ref([
  {
    name: 'weixin',
    title: '微信小程序',
    icon: '💚',
    color: 'text-green-600',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    features: ['支持企业微信', 'CI机器人选择', '编译设置', '代码压缩保护'],
  },
  {
    name: 'alipay',
    title: '支付宝小程序',
    icon: '💙',
    color: 'text-blue-600',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200',
    features: ['多终端支持', '版本号自增', '私钥认证', '开放平台集成'],
  },
  {
    name: 'dd',
    title: '钉钉小程序',
    icon: '💜',
    color: 'text-purple-600',
    bgColor: 'bg-purple-50',
    borderColor: 'border-purple-200',
    features: ['企业应用', '版本号自增', 'Token认证', '多应用类型'],
  },
])

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
          🚀
        </view>
        <view class="mb-2 text-6 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          uni-mini-ci
        </view>
        <view class="mb-2 text-3.5 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          小程序持续集成的插件
        </view>
        <view class="text-3 text-gray-500 dark:text-[var(--wot-dark-color2)]">
          支持上传微信、企业微信、钉钉、支付宝平台的小程序
        </view>
      </view>
    </view>

    <!-- 核心特性 -->
    <demo-block title="核心特性" transparent>
      <view class="grid grid-cols-2 gap-3">
        <view
          v-for="feature in features"
          :key="feature.title"
          class="rounded-2 bg-white p-4 text-center dark:bg-[var(--wot-dark-background2)]"
        >
          <view class="mb-2 text-6">
            {{ feature.icon }}
          </view>
          <view class="mb-1 text-3.5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            {{ feature.title }}
          </view>
          <view class="text-3 text-gray-600 leading-snug dark:text-[var(--wot-dark-color2)]">
            {{ feature.desc }}
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 安装方式 -->
    <demo-block title="安装方式" transparent>
      <view class="space-y-4">
        <!-- 全局安装 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            全局安装
          </view>
          <view class="mb-3 text-3 text-gray-600 dark:text-[var(--wot-dark-color2)]">
            推荐在开发环境中全局安装，方便在任何项目中使用
          </view>
          <view class="space-y-2">
            <view class="flex items-center justify-between border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode('npm i uni-mini-ci -g')">
              <text class="flex-1 text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
                npm i uni-mini-ci -g
              </text>
              <wd-icon name="copy" size="16px" color="#666" />
            </view>
          </view>
        </view>

        <!-- 局部安装 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            局部安装
          </view>
          <view class="mb-3 text-3 text-gray-600 dark:text-[var(--wot-dark-color2)]">
            在项目中作为开发依赖安装，适合团队协作
          </view>
          <view class="space-y-2">
            <view class="flex items-center justify-between border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode('npm i uni-mini-ci --save-dev')">
              <text class="flex-1 text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
                npm i uni-mini-ci --save-dev
              </text>
              <wd-icon name="copy" size="16px" color="#666" />
            </view>
            <view class="flex items-center justify-between border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode('pnpm add uni-mini-ci -D')">
              <text class="flex-1 text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
                pnpm add uni-mini-ci -D
              </text>
              <wd-icon name="copy" size="16px" color="#666" />
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 配置文件 -->
    <demo-block title="配置文件" transparent>
      <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          .minicirc 配置文件
        </view>
        <view class="mb-3 text-3 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          在项目根目录创建 <text class="rounded bg-gray-100 px-1 font-mono dark:bg-[var(--wot-dark-background3)]">
            .minicirc
          </text> 文件，配置各平台的上传参数
        </view>

        <view class="mb-3 border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode(configExample)">
          <view class="mb-2 flex items-center justify-between">
            <text class="text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              配置示例:
            </text>
            <wd-icon name="copy" size="16px" color="#666" />
          </view>
          <view class="max-h-60 overflow-y-auto">
            <pre class="whitespace-pre-wrap text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">{{ configExample }}</pre>
          </view>
        </view>

        <view class="border border-orange-200 rounded-2 bg-orange-50 p-3 dark:bg-orange-900/20">
          <view class="mb-2 text-3.5 text-orange-700 font-bold dark:text-orange-300">
            💡 配置说明
          </view>
          <view class="text-3 text-orange-600 leading-relaxed space-y-1 dark:text-orange-200">
            <view>• version: 上传版本号，不传时默认读取 package.json 的 version 字段</view>
            <view>• desc: 上传时的描述信息</view>
            <view>• autoincrement: 版本号自增，建议测试环境开启</view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 支持平台 -->
    <demo-block title="支持平台" transparent>
      <view class="space-y-3">
        <view
          v-for="platform in platforms"
          :key="platform.name"
          class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]"
        >
          <view class="mb-3 flex items-center">
            <view class="mr-2 text-6">
              {{ platform.icon }}
            </view>
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              {{ platform.title }}
            </view>
          </view>
          <view class="grid grid-cols-2 mb-3 gap-2">
            <view
              v-for="feature in platform.features"
              :key="feature"
              class="rounded bg-gray-100 px-2 py-1 text-center text-2.5 text-gray-600 dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]"
            >
              {{ feature }}
            </view>
          </view>
          <view class="flex items-center justify-between border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode(`minici --platform ${platform.name}`)">
            <text class="flex-1 text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
              minici --platform {{ platform.name }}
            </text>
            <wd-icon name="copy" size="16px" color="#666" />
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 添加命令 -->
    <demo-block title="添加命令" transparent>
      <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          package.json 脚本配置
        </view>
        <view class="mb-3 text-3 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          在 package.json 中添加上传脚本，支持单独上传和打包上传组合
        </view>

        <view class="mb-3 border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode(packageScripts)">
          <view class="mb-2 flex items-center justify-between">
            <text class="text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              脚本配置:
            </text>
            <wd-icon name="copy" size="16px" color="#666" />
          </view>
          <view class="max-h-60 overflow-y-auto">
            <pre class="whitespace-pre-wrap text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">{{ packageScripts }}</pre>
          </view>
        </view>

        <view class="space-y-2">
          <view class="text-3.5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            使用命令:
          </view>
          <view class="grid grid-cols-1 gap-2">
            <view class="flex items-center justify-between border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode('pnpm upload:weixin')">
              <text class="flex-1 text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
                pnpm upload:weixin
              </text>
              <wd-icon name="copy" size="16px" color="#666" />
            </view>
            <view class="flex items-center justify-between border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]" @click="copyCode('pnpm upload:mp-weixin')">
              <text class="flex-1 text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
                pnpm upload:mp-weixin
              </text>
              <wd-icon name="copy" size="16px" color="#666" />
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 使用步骤 -->
    <demo-block title="使用步骤" transparent>
      <view class="space-y-3">
        <view
          v-for="(step, index) in [
            { title: '安装插件', desc: '选择全局或局部安装方式', icon: '📦' },
            { title: '创建配置', desc: '在根目录创建 .minicirc 配置文件', icon: '⚙️' },
            { title: '配置平台', desc: '填写各平台的 appid、密钥等信息', icon: '🔑' },
            { title: '添加脚本', desc: '在 package.json 中添加上传命令', icon: '📝' },
            { title: '执行上传', desc: '运行命令上传到对应平台', icon: '🚀' },
          ]"
          :key="index"
          class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]"
        >
          <view class="flex items-center">
            <view class="mr-3 h-8 w-8 flex items-center justify-center rounded-full bg-blue-100 text-3.5 text-blue-600 font-bold dark:bg-blue-900/20 dark:text-blue-400">
              {{ index + 1 }}
            </view>
            <view class="mr-2 text-5">
              {{ step.icon }}
            </view>
            <view class="flex-1">
              <view class="text-3.5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
                {{ step.title }}
              </view>
              <view class="text-3 text-gray-600 dark:text-[var(--wot-dark-color2)]">
                {{ step.desc }}
              </view>
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 注意事项 -->
    <demo-block title="注意事项" transparent>
      <view class="space-y-3">
        <view class="border border-red-200 rounded-2 bg-red-50 p-4 dark:bg-red-900/20">
          <view class="mb-2 text-3.5 text-red-700 font-bold dark:text-red-300">
            ⚠️ 版本号限制
          </view>
          <view class="text-3 text-red-600 leading-relaxed dark:text-red-200">
            支付宝和钉钉小程序不支持上传的版本号小于或等于现有版本号。建议测试环境开启 autoincrement 字段，生产环境手动指定版本号。
          </view>
        </view>

        <view class="border border-blue-200 rounded-2 bg-blue-50 p-4 dark:bg-blue-900/20">
          <view class="mb-2 text-3.5 text-blue-700 font-bold dark:text-blue-300">
            💡 最佳实践
          </view>
          <view class="text-3 text-blue-600 leading-relaxed space-y-1 dark:text-blue-200">
            <view>• 测试环境：开启版本号自增，频繁调试更方便</view>
            <view>• 生产环境：手动指定版本号，便于版本管理</view>
            <view>• 密钥安全：不要将私钥文件提交到代码仓库</view>
            <view>• CI/CD：结合打包命令，实现自动化部署</view>
          </view>
        </view>

        <view class="border border-green-200 rounded-2 bg-green-50 p-4 dark:bg-green-900/20">
          <view class="mb-2 text-3.5 text-green-700 font-bold dark:text-green-300">
            🔒 安全建议
          </view>
          <view class="text-3 text-green-600 leading-relaxed space-y-1 dark:text-green-200">
            <view>• 使用环境变量存储敏感信息</view>
            <view>• 将配置文件添加到 .gitignore</view>
            <view>• 定期更换密钥和 Token</view>
            <view>• 限制 CI 机器人权限范围</view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 相关链接 -->
    <demo-block title="相关链接" transparent>
      <wd-cell-group border custom-class="rounded-2! overflow-hidden">
        <wd-cell title="📦 NPM 包" value="uni-mini-ci" is-link @click="handleNavigate('https://www.npmjs.com/package/uni-mini-ci')" />
        <wd-cell title="🐙 GitHub 仓库" value="源码仓库" is-link @click="handleNavigate('https://github.com/Moonofweisheng/uni-mini-ci')" />
        <wd-cell title="📱 微信小程序 CI" value="官方文档" is-link @click="handleNavigate('https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html')" />
        <wd-cell title="💙 支付宝小程序 CI" value="官方文档" is-link @click="handleNavigate('https://opendocs.alipay.com/mini/02q29z')" />
        <wd-cell title="💜 钉钉小程序 CI" value="官方文档" is-link @click="handleNavigate('https://github.com/open-dingtalk/dingtalk-design-cli')" />
      </wd-cell-group>
    </demo-block>
  </view>
</template>
