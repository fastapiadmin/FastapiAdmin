<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useI18n } from 'vue-i18n'

interface Props {
  title?: string // 标题
  desc?: string // 描述
  subDesc?: string // 字描述
  protocol?: string // 协议名称
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  desc: '',
  subDesc: '',
  protocol: '',
})

const { t } = useI18n()
const titleText = computed(() => props.title || t('privacy.title'))
const descText = computed(() => props.desc || t('privacy.desc'))
const subDescText = computed(() => props.subDesc || t('privacy.subDesc'))
const protocolText = computed(() => props.protocol || t('privacy.protocol'))

const emit = defineEmits(['agree', 'disagree'])
const showPopup = ref<boolean>(false) // 是否展示popup

const privacyResolves = ref(new Set()) // onNeedPrivacyAuthorization的reslove

function privacyHandler(resolve: any) {
  showPopup.value = true
  privacyResolves.value.add(resolve)
}

onBeforeMount(() => {
  // 注册监听
  if (typeof wx !== 'undefined' && wx.onNeedPrivacyAuthorization) {
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
  if (typeof wx !== 'undefined' && wx.openPrivacyContract)
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
          {{ titleText }}
        </view>
      </view>
      <view class="wd-privacy-popup__container">
        <wd-text :text="descText" />
        <wd-text class="wd-privacy-popup__container-protocol" :text="protocolText" @click="openPrivacyContract" />
        <wd-text :text="subDescText" />
      </view>
      <view class="wd-privacy-popup__footer">
        <button id="disagree-btn" class="is-block is-round is-medium is-plain wd-privacy-popup__footer-disagree wd-button" @click="handleDisagree">
          {{ t('privacy.disagree') }}
        </button>
        <button
          id="agree-btn"
          class="wd-button is-block is-round is-medium is-primary wd-privacy-popup__footer-agree"
          open-type="agreePrivacyAuthorization"
          @agreeprivacyauthorization="handleAgree"
        >
          {{ t('privacy.agree') }}
        </button>
      </view>
    </wd-popup>
  </view>
</template>

<style lang="scss">
// 非 scoped：wd-popup 通过 custom-class 传入根类名，弹窗挂载层级不受组件作用域约束，
// :deep() 在小程序端对 virtualHost 组件不可靠，改用全局类名直接命中（H5/MP 均生效）
.wd-privacy-popup {
  width: 600rpx;
  padding: 0 24rpx;
  box-sizing: border-box;
  border-radius: var(--fa-radius-md, 24rpx);
  overflow: hidden;
}
</style>

<style lang="scss" scoped>
.wd-privacy-popup {
  &__header {
    width: 100%;
    height: 128rpx;
    line-height: 128rpx;
    @apply wot-text-text-main;
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
    @apply wot-text-text-secondary;
    text-align: left;
    font-weight: 550;
    &-protocol {
      @apply wot-text-primary-6;
    }
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    padding-bottom: 36rpx;

    /* 组件 wxss 不允许标签选择器（微信小程序限制），改用类选择器 */
    &-disagree,
    &-agree {
      border: none;
      outline: none;
    }
  }
}
</style>
