<script lang="ts" setup>
import { onBeforeMount, ref } from 'vue'

interface Props {
  title?: string // 标题
  desc?: string // 描述
  subDesc?: string // 字描述
  protocol?: string // 协议名称
}

withDefaults(defineProps<Props>(), {
  title: '用户隐私保护提示',
  desc: '感谢您使用本应用，您使用本应用的服务之前请仔细阅读并同意',
  subDesc: '。当您点击同意并开始时用产品服务时，即表示你已理解并同意该条款内容，该条款将对您产生法律约束力。如您拒绝，将无法使用相应服务。',
  protocol: '《用户隐私保护指引》',
})

const emit = defineEmits(['agree', 'disagree'])
const showPopup = ref<boolean>(false) // 是否展示popup

const privacyResolves = ref(new Set()) // onNeedPrivacyAuthorization的reslove

function privacyHandler(resolve: any) {
  showPopup.value = true
  privacyResolves.value.add(resolve)
}

onBeforeMount(() => {
  // 注册监听
  if (wx.onNeedPrivacyAuthorization) {
    wx.onNeedPrivacyAuthorization((resolve: any) => {
      if (typeof privacyHandler === 'function') {
        privacyHandler(resolve)
      }
    })
  }
})

/**
 * 同意隐私协议
 */
function handleAgree() {
  showPopup.value = false
  privacyResolves.value.forEach((resolve: any) => {
    resolve({
      event: 'agree',
      buttonId: 'agree-btn',
    })
  })
  privacyResolves.value.clear()
  emit('agree')
}

/**
 * 拒绝隐私协议
 */
function handleDisagree() {
  showPopup.value = false
  privacyResolves.value.forEach((resolve: any) => {
    resolve({
      event: 'disagree',
    })
  })
  privacyResolves.value.clear()
}

/**
 * 打开隐私协议
 */
function openPrivacyContract() {
  wx.openPrivacyContract({})
}

/**
 * 弹出框关闭时清空
 */
function handleClose() {
  privacyResolves.value.clear()
}
</script>

<script lang="ts">
export default {
  options: {
    virtualHost: true,
    addGlobalClass: true,
    styleIsolation: 'shared',
  },
}
</script>

<template>
  <view>
    <wd-popup v-model="showPopup" :close-on-click-modal="false" custom-class="wd-privacy-popup" @close="handleClose">
      <view class="wd-privacy-popup__header">
        <!-- 标题 -->
        <view class="wd-picker__title">
          {{ title }}
        </view>
      </view>
      <view class="wd-privacy-popup__container">
        <text>{{ desc }}</text>
        <text class="wd-privacy-popup__container-protocol" @click="openPrivacyContract">
          {{ protocol }}
        </text>
        <text>{{ subDesc }}</text>
      </view>
      <view class="wd-privacy-popup__footer">
        <button id="disagree-btn" class="is-block is-round is-medium is-plain wd-privacy-popup__footer-disagree wd-button" @click="handleDisagree">
          拒绝
        </button>
        <button
          id="agree-btn"
          class="wd-button is-block is-round is-medium is-primary wd-privacy-popup__footer-agree"
          open-type="agreePrivacyAuthorization"
          @agreeprivacyauthorization="handleAgree"
        >
          同意
        </button>
      </view>
    </wd-popup>
  </view>
</template>

<style lang="scss" scoped>
@import 'wot-design-uni/components/wd-button/index.scss';
:deep(.wd-privacy-popup) {
  width: 600rpx;
  padding: 0 24rpx;
  box-sizing: border-box;
  border-radius: 32rpx;
  overflow: hidden;
}

.wd-privacy-popup {
  &__header {
    width: 100%;
    height: 128rpx;
    line-height: 128rpx;
    color: rgba(0, 0, 0, 0.85);
    font-size: 30rpx;
    padding: 0 12rpx;
    box-sizing: border-box;
  }

  &__container {
    width: 100%;
    box-sizing: border-box;
    padding: 0 12rpx;
    margin-bottom: 32rpx;

    font-size: 28rpx;
    line-height: 1.8;
    color: #3e3e3e;
    text-align: left;
    font-weight: 550;
    &-protocol {
      color: #4d80f0;
    }
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    padding-bottom: 36rpx;

    button {
      border: none;
      outline: none;
    }
  }
}
</style>
