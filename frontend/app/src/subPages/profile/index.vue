<script setup lang="ts">
import type { FormRules } from 'wot-design-uni/components/wd-form/types'
import type { UserInfo } from '@/api/user'
import { onLoad } from '@dcloudio/uni-app'
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import UserAPI from '@/api/user'
// 移除了 FileAPI 导入，该模块不存在
import { useUserStore } from '@/store/userStore'

definePage({
  name: 'profile',
  style: {
    navigationBarTitleText: '个人中心',
  },
})

const userStore = useUserStore()

const originalSrc = ref<string>('') // 选取的原图路径
const avatarShow = ref<boolean>(false) // 显示头像裁剪
const userProfile = ref<UserInfo>() // 用户信息

/** 加载用户信息 */
async function loadUserProfile() {
  userProfile.value = await UserAPI.getCurrentUserInfo()
}

// 头像选择
function avatarUpload() {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      originalSrc.value = res.tempFilePaths[0]
      avatarShow.value = true
    },
  })
}
// 头像裁剪完成
function handleAvatarConfirm(event: any) {
  const { tempFilePath } = event
  // 使用 UserAPI 的头像上传方法
  UserAPI.uploadCurrentUserAvatar({ file: tempFilePath }).then(
    (fileInfo: UploadFileResult) => {
      const avatarForm = {
        name: userProfile.value?.name || '',
        gender: userProfile.value?.gender || '0',
        mobile: userProfile.value?.mobile || '',
        email: userProfile.value?.email || '',
        username: userProfile.value?.username || '',
        dept_name: userProfile.value?.dept_name || '',
        positions: userProfile.value?.positions || [],
        roles: userProfile.value?.roles || [],
        avatar: fileInfo.file_url,
        created_at: userProfile.value?.created_at || '',
      }
      // 头像路径保存至后端
      UserAPI.updateCurrentUserInfo(avatarForm).then(() => {
        uni.showToast({ title: '头像上传成功', icon: 'none' })
        loadUserProfile()
      })
    },
  )
}

// 本页面中所有的校验规则
const rules: FormRules = {
  name: [{ required: true, message: '请填写昵称' }],
  gender: [{ required: true, message: '请选择性别' }],
}

const dialog = reactive<{
  visible: boolean
  title?: string
  field?: string
}>({
  visible: false,
})

const userProfileForm = reactive<{
  name?: string
  gender?: string
}>({})
const userProfileFormRef = ref()

// 打开弹窗
function handleOpenDialog(field: string) {
  dialog.field = field
  dialog.visible = true

  // 初始化表单数据
  if (field === 'name') {
    dialog.title = '编辑昵称'
    userProfileForm.name = userProfile.value?.name || ''
  }
  else if (field === 'gender') {
    dialog.title = '选择性别'
    userProfileForm.gender = userProfile.value?.gender || '0'
  }
}

// 提交表单
function handleSubmit() {
  userProfileFormRef.value.validate().then(({ valid }: { valid: boolean }) => {
    if (valid) {
      UserAPI.updateCurrentUserInfo({
        name: userProfileForm.name,
        gender: userProfileForm.gender,
        mobile: userProfile.value?.mobile || '',
        email: userProfile.value?.email || '',
        username: userProfile.value?.username || '',
        dept_name: userProfile.value?.dept_name || '',
        positions: userProfile.value?.positions || [],
        roles: userProfile.value?.roles || [],
        avatar: userProfile.value?.avatar || '',
        created_at: userProfile.value?.created_at || '',
      }).then(() => {
        uni.showToast({ title: '账号资料修改成功', icon: 'none' })
        dialog.visible = false
        loadUserProfile()
      })
    }
  })
}

// 检查登录状态
onLoad(() => {
  if (!userStore.checkLogin())
    return

  // #ifdef H5
  document.addEventListener('touchstart', touchstartListener, {
    passive: false,
  })
  document.addEventListener('touchmove', touchmoveListener, { passive: false })
  // #endif
  loadUserProfile()
})

onMounted(() => {
  // 在onMounted中不再重复检查登录状态和加载用户信息
  // 如果需要检查登录状态和加载用户信息，请使用onLoad中的逻辑
})

// 页面销毁前移除事件监听
onBeforeUnmount(() => {
  // #ifdef H5
  document.removeEventListener('touchstart', touchstartListener)
  document.removeEventListener('touchmove', touchmoveListener)
  // #endif
})
// 禁用浏览器双指缩放，使头像裁剪时双指缩放能够起作用
function touchstartListener(event: TouchEvent) {
  if (event.touches.length > 1) {
    event.preventDefault()
  }
}
// 禁用浏览器下拉刷新，使头像裁剪时能够移动图片
function touchmoveListener(event: TouchEvent) {
  event.preventDefault()
}
</script>

<template>
  <view class="app-container">
    <wd-card
      v-if="userProfile"
      custom-style="margin-top: 20rpx"
      class="theme-card"
    >
      <wd-cell-group border>
        <wd-cell
          class="avatar-cell"
          title="头像"
          center
          is-link
          @click="avatarUpload"
        >
          <template #title>
            <text class="theme-text-primary">
              头像
            </text>
          </template>
          <view class="avatar flex-center">
            <view
              v-if="!userProfile.avatar"
              class="img flex-center"
              @click="avatarUpload"
            >
              <wd-icon
                name="fill-camera"
                custom-class="img-icon"
              />
            </view>
            <wd-img
              v-if="userProfile.avatar"
              round
              width="80px"
              height="80px"
              :src="userProfile.avatar"
              mode="aspectFit"
              custom-class="profile-img"
              @click="avatarUpload"
            />
          </view>
        </wd-cell>
        <wd-cell
          title="昵称"
          :value="userProfile.name"
          is-link
          @click="handleOpenDialog('name')"
        >
          <template #title>
            <text class="theme-text-primary">
              昵称
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.name || "未设置"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell
          title="性别"
          :value="
            userProfile.gender === '0'
              ? '男'
              : userProfile.gender === '1'
                ? '女'
                : '未知'
          "
          is-link
          @click="handleOpenDialog('gender')"
        >
          <template #title>
            <text class="theme-text-primary">
              性别
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.gender === "0"
                  ? "男"
                  : userProfile.gender === "1"
                    ? "女"
                    : "未知"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell title="用户名" :value="userProfile.username">
          <template #title>
            <text class="theme-text-primary">
              用户名
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{ userProfile.username }}
            </text>
          </template>
        </wd-cell>
        <wd-cell v-if="userProfile" title="状态" center>
          <template #title>
            <text class="theme-text-primary">
              状态
            </text>
          </template>
          <wd-tag :type="userProfile.status ? 'success' : 'danger'">
            {{ userProfile.status ? "启用" : "停用" }}
          </wd-tag>
        </wd-cell>
        <wd-cell v-if="userProfile" title="是否超管" center>
          <template #title>
            <text class="theme-text-primary">
              是否超管
            </text>
          </template>
          <wd-tag
            plain
            :type="userProfile.is_superuser ? 'primary' : 'default'"
          >
            {{ userProfile.is_superuser ? "是" : "否" }}
          </wd-tag>
        </wd-cell>
        <wd-cell title="手机号" :value="userProfile.mobile">
          <template #title>
            <text class="theme-text-primary">
              手机号
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.mobile || "未绑定"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell title="邮箱" :value="userProfile.email">
          <template #title>
            <text class="theme-text-primary">
              邮箱
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.email || "未绑定"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell title="部门" :value="userProfile.dept_name">
          <template #title>
            <text class="theme-text-primary">
              部门
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.dept_name || "未分配"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell
          title="角色"
          :value="userProfile.roles?.map((item) => item.name).join(', ')"
        >
          <template #title>
            <text class="theme-text-primary">
              角色
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.roles?.map((item) => item.name).join(", ")
                  || "未分配"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell
          title="岗位"
          :value="userProfile.positions?.map((item) => item.name).join(', ')"
        >
          <template #title>
            <text class="theme-text-primary">
              岗位
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.positions?.map((item) => item.name).join(", ")
                  || "未分配"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell title="备注" :value="userProfile.description">
          <template #title>
            <text class="theme-text-primary">
              备注
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.description || "无"
              }}
            </text>
          </template>
        </wd-cell>
        <wd-cell title="创建日期" :value="userProfile.created_at">
          <template #title>
            <text class="theme-text-primary">
              创建日期
            </text>
          </template>
          <template #value>
            <text class="theme-text-secondary">
              {{
                userProfile.created_at
              }}
            </text>
          </template>
        </wd-cell>
      </wd-cell-group>
    </wd-card>

    <!-- 头像裁剪 -->
    <wd-img-cropper
      v-model="avatarShow"
      :img-src="originalSrc"
      @confirm="handleAvatarConfirm"
    />

    <!-- 用户信息编辑弹出框 -->
    <wd-popup
      v-model="dialog.visible"
      position="bottom"
      custom-style="border-top-left-radius: 16rpx; border-top-right-radius: 16rpx;"
    >
      <view class="popup-header">
        <wd-cell :title="dialog.title" center>
          <template #right-icon>
            <wd-icon name="close" size="20" @click="dialog.visible = false" />
          </template>
        </wd-cell>
      </view>

      <wd-divider />

      <wd-form
        ref="userProfileFormRef"
        :model="userProfileForm"
        custom-class="edit-form"
      >
        <wd-cell-group border>
          <wd-input
            v-if="dialog.field === 'name'"
            v-model="userProfileForm.name"
            label="昵称"
            label-width="160rpx"
            placeholder="请输入昵称"
            prop="name"
            :rules="rules.name"
          />
          <wd-cell
            v-if="dialog.field === 'gender'"
            title="性别"
            title-width="160rpx"
            center
            prop="gender"
            :rules="rules.gender"
          >
            <wd-radio-group
              v-model="userProfileForm.gender"
              shape="button"
              class="ef-radio-group"
            >
              <wd-radio :value="0">
                男
              </wd-radio>
              <wd-radio :value="1">
                女
              </wd-radio>
              <wd-radio :value="2">
                未知
              </wd-radio>
            </wd-radio-group>
          </wd-cell>
        </wd-cell-group>
        <view>
          <wd-button type="primary" block @click="handleSubmit">
            提交
          </wd-button>
        </view>
      </wd-form>
    </wd-popup>
  </view>
</template>

<style lang="scss" scoped>
.avatar-cell {
  :deep(.wd-cell__body) {
    align-items: center;
  }

  .avatar {
    display: flex;
    align-items: center;
    justify-content: right;

    .img {
      position: relative;
      width: 80px;
      height: 80px;
      background-color: rgba(0, 0, 0, 0.04);
      border-radius: 50%;

      .img-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        color: #fff;
      }
    }
  }
}

.edit-form {
  padding-top: 40rpx;

  .ef-radio-group {
    line-height: 1;
    text-align: left;
  }
}
</style>
