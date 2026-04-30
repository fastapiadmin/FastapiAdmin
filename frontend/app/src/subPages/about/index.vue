<script setup lang="ts">
definePage({
  name: 'about',
  style: {
    navigationBarTitleText: '关于',
  },
})

// 核心团队成员
const coreTeam = [
  {
    name: '不如摸鱼去',
    avatar: 'https://avatars.githubusercontent.com/u/26426873?v=4',
    role: '前端打工仔',
    desc: '负责WotUI组件库的开发和维护',
    github: 'https://github.com/Moonofweisheng',
  },
  {
    name: '二狗',
    avatar: 'https://avatars.githubusercontent.com/u/50100966?v=4',
    role: '灵活就业大师',
    desc: '问题毁灭者，总能迅速解决各种技术难题',
    github: 'https://github.com/810505339',
  },
  {
    name: 'RJQingHuan',
    avatar: 'https://avatars.githubusercontent.com/u/53939074?v=4',
    role: 'Pull Shark',
    desc: '热衷参与开源组件建设',
    github: 'https://github.com/RJQingHuan',
  },
  {
    name: 'skiyee',
    avatar: 'https://avatars.githubusercontent.com/u/120664167?v=4',
    role: 'uni-ku 的创立者，重金雇佣兵',
    desc: '精通 JS 和 TS 的全能攻城狮',
    github: 'https://github.com/skiyee',
  },
  {
    name: 'jasper-ops',
    avatar: 'https://avatars.githubusercontent.com/u/85024227?v=4',
    role: '新技术狂热分子',
    desc: '始终走在技术前沿，热衷于探索最新的开发趋势',
    github: 'https://github.com/jasper-ops',
  },
]

function openUrl(url: string) {
  window.open(url, '_blank')
}

// 打开公众号二维码
function openWeChat() {
  uni.previewImage({
    urls: ['https://wot-ui.cn/wechatPublicAccount.png'],
  })
}

// 打开捐赠二维码
function donate() {
  uni.previewImage({
    urls: ['https://wot-ui.cn/weixinQrcode.jpg'],
  })
}
</script>

<template>
  <view class="min-h-screen bg-gray-100 py-3 dark:bg-[var(--wot-dark-background)]">
    <!-- 头部介绍 -->
    <view class="mx-3 mb-3 flex flex-col gap-2">
      <text class="text-6 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
        关于我们
      </text>
      <text class="text-3.5 text-gray-600 leading-snug dark:text-[var(--wot-dark-color2)]">
        我是不如摸鱼去，一个前端打工仔，我和我的小伙伴们正在致力于开发轻量、高效的uni-app组件库和高效、易用的uni-app快速开发模板。
      </text>
    </view>

    <!-- 核心团队 -->
    <demo-block title="核心团队" transparent>
      <view class="grid grid-cols-2 gap-3">
        <view
          v-for="member in coreTeam"
          :key="member.name"
          class="rounded-2 bg-white p-4 text-center dark:bg-[var(--wot-dark-background2)]"
          @click="openUrl(member.github)"
        >
          <image
            :src="member.avatar"
            class="mx-auto mb-2 h-16 w-16 border-2 border-blue-200 rounded-full dark:border-blue-800"
          />
          <view class="mb-1 text-3.5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            {{ member.name }}
          </view>
          <view class="mb-2 text-2.5 text-blue-600 dark:text-blue-400">
            {{ member.role }}
          </view>
          <view class="text-2.5 text-gray-600 leading-snug dark:text-[var(--wot-dark-color2)]">
            {{ member.desc }}
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 关于 uni-helper -->
    <demo-block title="关于 uni-helper 团队" transparent>
      <view class="rounded-3 bg-white p-5 dark:bg-[var(--wot-dark-background2)]">
        <text class="mb-3 block text-3.5 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          <text class="text-blue-600" @click="openUrl('https://uni-helper.cn/')">
            uni-helper
          </text>
          是一个旨在增强 uni-app 系列产品的开发体验为爱发电的非官方组织。作为靠爱发电的非官方项目，uni-helper 提供了打包工具插件支持、编辑器扩展支持、NPM 包等并尽力维护它们。
        </text>
        <text class="text-3.5 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          在此我们特别向 uni-helper 团队表示感谢，他们为 uni-app 系列产品提供了强大的支持，包括打包工具插件支持、编辑器扩展支持等，这使我们得以站在巨人的巨人的肩膀上完成此项目。
        </text>
      </view>
    </demo-block>

    <!-- 更多信息 -->
    <demo-block title="更多信息" transparent>
      <wd-cell-group border custom-class="rounded-2! overflow-hidden">
        <wd-cell
          title="关注公众号"
          title-width="200px"
          label="uni-app教程、组件库讯息一手掌握！"
          is-link
          @click="openWeChat"
        />
        <wd-cell
          title="捐赠"
          title-width="200px"
          label="每一份捐赠都是对我们莫大的鼓励！"
          is-link
          @click="donate"
        />
      </wd-cell-group>
    </demo-block>
  </view>
</template>
