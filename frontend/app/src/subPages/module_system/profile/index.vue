<script setup lang="ts">
import type { UploadMethod } from '@wot-ui/ui/components/wd-upload/types'
import type { UserInfo, UserProfileForm } from '@/api/module_system/user'
import { onLoad } from '@dcloudio/uni-app'
import { computed, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import UserAPI from '@/api/module_system/user'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useUserStore } from '@/store/userStore'

definePage({
  name: 'profile',
  layout: 'default',
  style: { navigationBarTitleText: '个人资料' },
})
useI18nNavTitle('profile.navTitle')

const { t } = useI18n()
const toast = useToast()
const userStore = useUserStore()

const loading = ref(false)
const loadError = ref(false)
const saving = ref(false)
const userProfile = ref<UserInfo>()

/**
 * 头像上传：交给统一 http 层处理（alova 适配器 `requestType: 'upload'` → uni.uploadFile）。
 *
 * 之前由页面自己拼 `VITE_API_BASE_URL + VITE_APP_BASE_API + /file/upload` 并手工设置
 * `Authorization`，有两个问题：
 * 1. 路径缺 `/common` 前缀，后端真实路径是 `/api/v1/common/file/upload`（404）；
 * 2. 绕过 http 层，拿不到统一的令牌注入与错误处理。
 * 现在通过 `wd-upload` 的 `upload-method` 钩子走 `UserAPI.uploadCurrentUserAvatar`，
 * 请求头由 http 层 `beforeRequest` 注入。
 */
const uploadAvatar: UploadMethod = async (uploadFile, formData, options) => {
  try {
    const res = await UserAPI.uploadCurrentUserAvatar({
      filePath: uploadFile.url,
      name: options.name || 'file',
    })
    // 与 wd-upload 默认上传保持一致：statusCode 命中 successStatus（默认 200）才算成功
    const successStatus = options.statusCode ?? 200
    const isSuccess = Array.isArray(successStatus)
      ? successStatus.includes(res.statusCode)
      : res.statusCode === successStatus

    if (isSuccess) {
      options.onSuccess(res, uploadFile, formData)
    }
    else {
      options.onError({ ...res, errMsg: res.errMsg || `HTTP ${res.statusCode}` }, uploadFile, formData)
    }
  }
  catch (error) {
    options.onError({ errMsg: (error as Error)?.message || 'upload failed' } as UniApp.GeneralCallbackResult, uploadFile, formData)
  }
}
const avatarFileList = ref<{ url: string }[]>([])

const genderText = computed(() => {
  const gender = userProfile.value?.gender
  return gender === '0' ? t('profile.male') : gender === '1' ? t('profile.female') : t('profile.unknown')
})
const deptText = computed(() => userProfile.value?.dept_name || '-')
const roleText = computed(() => {
  const names = userProfile.value?.role_names?.filter(Boolean)
  if (names?.length)
    return names.join('、')
  const roles = userProfile.value?.roles?.map(role => role.name).filter(Boolean)
  return roles?.length ? roles.join('、') : '-'
})

async function loadUserProfile() {
  loading.value = true
  loadError.value = false
  try {
    userProfile.value = await UserAPI.getCurrentUserInfo()
  }
  catch {
    // http 层已统一错误提示，页面保留错误态与重试入口
    loadError.value = true
  }
  finally {
    loading.value = false
  }
}

/** 保存个人资料（昵称/性别/头像变更均走此接口） */
async function saveProfile(patch: Partial<UserProfileForm>) {
  const profile = userProfile.value
  if (!profile)
    return
  saving.value = true
  try {
    await UserAPI.updateCurrentUserInfo({
      name: patch.name ?? profile.name ?? '',
      gender: patch.gender ?? profile.gender ?? '0',
      mobile: profile.mobile || '',
      email: profile.email || '',
      username: profile.username || '',
      dept_name: profile.dept_name || '',
      positions: profile.positions || [],
      roles: profile.roles || [],
      avatar: patch.avatar ?? (profile.avatar || ''),
    })
    toast.success(t('common.saveSuccess'))
    await loadUserProfile()
    // 同步全局用户信息，使「我的」页展示最新昵称/头像
    userStore.setUserInfo({ ...userStore.userInfo, ...patch })
  }
  catch {
    // http 层已统一错误提示
  }
  finally {
    saving.value = false
  }
}

/** 头像上传成功：wd-upload 的 response 为字符串，解析后保存 */
function handleAvatarSuccess(e: { file: { response?: string | Record<string, any> } }) {
  try {
    const raw = typeof e.file.response === 'string' ? e.file.response : JSON.stringify(e.file.response || {})
    const res = JSON.parse(raw) as { code: number, msg?: string, data?: { file_url?: string } }
    if (res.code === 0 && res.data?.file_url) {
      avatarFileList.value = []
      saveProfile({ avatar: res.data.file_url })
    }
    else {
      toast.error(res.msg || t('profile.uploadFailed'))
      avatarFileList.value = []
    }
  }
  catch {
    toast.error(t('profile.uploadFailed'))
    avatarFileList.value = []
  }
}
function handleAvatarFail() {
  toast.error(t('profile.uploadFailed'))
  avatarFileList.value = []
}

/** 昵称 / 性别编辑弹窗 */
const editDialog = reactive<{ visible: boolean, field: 'name' | 'gender' }>({ visible: false, field: 'name' })
const editForm = reactive<{ name: string, gender: string }>({ name: '', gender: '0' })
const editTitle = computed(() => editDialog.field === 'name' ? t('profile.editNickname') : t('profile.selectGender'))

function openEdit(field: 'name' | 'gender') {
  editDialog.field = field
  editDialog.visible = true
  if (field === 'name')
    editForm.name = userProfile.value?.name || ''
  else
    editForm.gender = userProfile.value?.gender || '0'
}

async function handleEditSubmit() {
  if (editDialog.field === 'name') {
    const name = editForm.name.trim()
    if (!name) {
      toast.warning(t('profile.nicknameRequired'))
      return
    }
    await saveProfile({ name })
  }
  else {
    await saveProfile({ gender: editForm.gender })
  }
  editDialog.visible = false
}

onLoad(() => {
  loadUserProfile()
})
</script>

<template>
  <view class="page-wraper py-3">
    <SkeletonPage v-if="loading && !userProfile" :rows="6" />

    <view v-else-if="loadError && !userProfile" class="mx-4 flex flex-col items-center gap-3 py-12">
      <wd-icon name="no-result" size="40px" color="var(--wot-text-auxiliary)" />
      <wd-text class="wot-text-text-secondary text-3.5" :text="t('profile.loadFailed')" />
      <wd-button size="small" plain @click="loadUserProfile">
        {{ t('common.retry') }}
      </wd-button>
    </view>

    <template v-else>
      <!-- 头像 + 昵称（点击头像即上传更换） -->
      <view class="mx-4 mb-6 flex flex-col items-center gap-2 py-4">
        <wd-upload
          v-model:file-list="avatarFileList"
          :upload-method="uploadAvatar"
          :limit="1"
          accept="image"
          :max-size="5242880"
          :source-type="['album', 'camera']"
          @success="handleAvatarSuccess"
          @fail="handleAvatarFail"
        >
          <view class="relative">
            <wd-avatar
              size="80px"
              round
              :src="userProfile?.avatar || ''"
              :text="(userProfile?.name || userProfile?.username || '?').charAt(0)"
            />
            <!-- 相机角标：示意可更换头像 -->
            <view
              class="wot-bg-primary-6 absolute h-6 w-6 flex items-center justify-center rounded-full -bottom-0.5 -right-0.5"
              style="border: 3rpx solid var(--wot-filled-content, #FFFFFF);"
            >
              <wd-icon name="camera" size="12px" color="#FFFFFF" />
            </view>
          </view>
        </wd-upload>
        <wd-text class="wot-text-text-main text-4" :text="userProfile?.name || userProfile?.username || '-'" bold />
      </view>

      <!-- 资料列表 -->
      <view class="mx-4 mb-6">
        <wd-cell-group border custom-class="rounded-3! overflow-hidden">
          <wd-cell :title="t('profile.nickname')" is-link @click="openEdit('name')">
            <wd-text class="wot-text-text-secondary" :text="userProfile?.name || t('profile.notSet')" />
          </wd-cell>
          <wd-cell :title="t('profile.gender')" is-link @click="openEdit('gender')">
            <wd-text class="wot-text-text-secondary" :text="genderText" />
          </wd-cell>
          <wd-cell :title="t('profile.username')" :value="userProfile?.username || '-'" />
          <wd-cell :title="t('profile.mobile')">
            <wd-text class="wot-text-text-secondary" :text="userProfile?.mobile || t('profile.notBound')" />
          </wd-cell>
          <wd-cell :title="t('profile.email')">
            <wd-text class="wot-text-text-secondary" :text="userProfile?.email || t('profile.notBound')" />
          </wd-cell>
          <wd-cell :title="t('profile.dept')" :value="deptText" />
          <wd-cell :title="t('profile.roles')" :value="roleText" />
        </wd-cell-group>
      </view>

      <!-- 昵称 / 性别编辑弹窗 -->
      <wd-popup
        v-model="editDialog.visible"
        position="bottom"
        round
        custom-style="padding-bottom: env(safe-area-inset-bottom);"
      >
        <view class="wot-text-text-main px-4 pb-4 pt-4 text-center text-4 font-bold">
          {{ editTitle }}
        </view>
        <view class="px-4 pb-4">
          <wd-input
            v-if="editDialog.field === 'name'"
            v-model="editForm.name"
            :placeholder="t('profile.nickname')"
            clearable
          />
          <wd-radio-group v-else v-model="editForm.gender" direction="horizontal">
            <wd-radio value="0">
              {{ t('profile.male') }}
            </wd-radio>
            <wd-radio value="1">
              {{ t('profile.female') }}
            </wd-radio>
          </wd-radio-group>
          <view class="mt-4">
            <wd-button type="primary" round block :loading="saving" @click="handleEditSubmit">
              {{ t('common.save') }}
            </wd-button>
          </view>
        </view>
        <wd-gap :height="20" />
      </wd-popup>
    </template>
  </view>
</template>
