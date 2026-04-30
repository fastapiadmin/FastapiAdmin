<script setup lang="ts">
import type { PasswordChangeForm, UserInfo } from '@/api/user'
import { computed, onMounted, reactive, ref } from 'vue'
import UserAPI from '@/api/user'

definePage({
  name: 'account',
  style: {
    navigationBarTitleText: '账号设置',
  },
})

const userProfile = ref<UserInfo>() // 用户信息
const passwordChangeForm = reactive<PasswordChangeForm>({
  old_password: '',
  new_password: '',
  confirm_password: '',
})
const passwordChangeFormRef = ref()

// 本页面中所有的校验规则
const rules = reactive({
  oldPassword: [{ required: true, message: '请填写原密码' }],
  newPassword: [{ required: true, message: '请填写新密码' }],
  confirmPassword: [
    {
      required: true,
      message: '请确认密码',
      validator: (value: string) => {
        if (!value) {
          return Promise.reject(new Error('请确认密码'))
        }
        else {
          if (value !== passwordChangeForm.new_password) {
            return Promise.reject(new Error('两次输入的密码不一致'))
          }
          else {
            return Promise.resolve()
          }
        }
      },
    },
  ],
  mobile: [
    {
      required: true,
      pattern: /^1[3-9]\d{9}$/,
      message: '请填写正确的手机号码',
    },
  ],
  code: [{ required: true, message: '请填写验证码' }],
  email: [
    {
      required: true,
      pattern: /\w[-\w.+]*@([A-Z0-9][-A-Z0-9]+\.)+[A-Z]{2,14}/i,
      message: '请填写正确的邮箱地址',
    },
  ],
})

enum DialogType {
  PASSWORD = 'password',
  MOBILE = 'mobile',
  EMAIL = 'email',
}

const dialog = reactive({
  visible: false,
  type: '' as DialogType,
})

const getDialogTitle = computed(() => {
  switch (dialog?.type) {
    case DialogType.PASSWORD:
      return '修改密码'
    case DialogType.MOBILE:
      return '绑定手机'
    case DialogType.EMAIL:
      return '绑定邮箱'
    default:
      return '账号设置'
  }
})

async function loadUserProfile() {
  userProfile.value = await UserAPI.getCurrentUserInfo()
}

/**
 * 打开弹窗
 * @param type 弹窗类型 ACCOUNT: 账号资料 PASSWORD: 修改密码 MOBILE: 绑定手机 EMAIL: 绑定邮箱
 */
function handleOpenDialog(type: DialogType) {
  dialog.type = type
  dialog.visible = true
  switch (type) {
    case DialogType.PASSWORD:
      passwordChangeForm.old_password = ''
      passwordChangeForm.new_password = ''
      passwordChangeForm.confirm_password = ''
      break
  }
}

// 提交表单
function handleSubmit() {
  if (dialog.type === DialogType.PASSWORD) {
    passwordChangeFormRef.value
      .validate()
      .then(({ valid }: { valid: boolean }) => {
        if (valid) {
          UserAPI.changeCurrentUserPassword(passwordChangeForm)
            .then(() => {
              uni.showToast({ title: '密码修改成功', icon: 'success' })
              dialog.visible = false
            })
            .catch((error: any) => {
              uni.showToast({
                title: error?.message || '密码修改失败',
                icon: 'error',
              })
            })
        }
      })
  }
}

onMounted(() => {
  loadUserProfile()
})
</script>

<template>
  <view class="app-container">
    <wd-card custom-style="margin-top: 20rpx" class="theme-card">
      <wd-cell-group border>
        <wd-cell
          title="账户密码"
          label="定期修改密码有助于保护账户安全"
          value="修改"
          is-link
          @click="handleOpenDialog(DialogType.PASSWORD)"
        >
          <template #title>
            <text class="theme-text-primary">
              账户密码
            </text>
          </template>
          <template #label>
            <text class="theme-text-secondary">
              定期修改密码有助于保护账户安全
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              修改
            </text>
          </template>
        </wd-cell>
      </wd-cell-group>
    </wd-card>

    <!-- 用户信息编辑弹出框 -->
    <wd-popup
      v-model="dialog.visible"
      position="bottom"
      custom-style="border-top-left-radius: 16rpx; border-top-right-radius: 16rpx;"
    >
      <view class="popup-header">
        <wd-cell :title="getDialogTitle" center>
          <template #right-icon>
            <wd-icon name="close" size="20" @click="dialog.visible = false" />
          </template>
        </wd-cell>
      </view>

      <wd-divider />

      <wd-form
        v-if="dialog.type === DialogType.PASSWORD"
        ref="passwordChangeFormRef"
        :model="passwordChangeForm"
        custom-class="edit-form"
      >
        <wd-cell-group border>
          <wd-input
            v-model="passwordChangeForm.old_password"
            label="原密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请输入原密码"
            prop="old_password"
            :rules="rules.oldPassword"
          />
          <wd-input
            v-model="passwordChangeForm.new_password"
            label="新密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请输入新密码"
            prop="new_password"
            :rules="rules.newPassword"
          />
          <wd-input
            v-model="passwordChangeForm.confirm_password"
            label="确认密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请确认新密码"
            prop="confirm_password"
            :rules="rules.confirmPassword"
          />
        </wd-cell-group>
        <view class="p-6">
          <wd-button type="primary" size="large" block @click="handleSubmit">
            提交
          </wd-button>
        </view>
      </wd-form>
    </wd-popup>
  </view>
</template>
