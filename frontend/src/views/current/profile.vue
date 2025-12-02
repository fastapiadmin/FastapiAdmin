<template>
  <div class="app-container">
    <el-row :gutter="12">
      <!-- 左侧信息卡片 -->
      <el-col :span="6" class="mb-4">
        <el-card :loading="loading" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>
          <div class="user-info-header">
            <div class="avatar-alert mb-10px">
              <!-- 提示：头像上传成功后请点击“保存更改”按钮才会生效 -->
              <el-alert
                type="info"
                show-icon
                :closable="false"
                title="头像上传，点击“保存更改”按钮使其生效"
              />
            </div>

            <div class="avatar-wrapper">
              <el-avatar v-if="infoFormState.avatar" :src="infoFormState.avatar" :size="120" />
              <el-avatar v-else icon="UserFilled" :size="120" />

              <el-upload
                ref="uploadRef"
                v-model:file-list="fileList"
                class="el-upload"
                name="file"
                :show-file-list="false"
                :before-upload="handleBeforeUpload"
                :http-request="handleUpload"
                :disabled="loading"
                :limit="1"
                :auto-upload="false"
                @change="handleFileChange"
              >
                <template #trigger>
                  <el-button type="primary" :icon="Camera" class="upload-trigger" />
                </template>
              </el-upload>
            </div>
            <span class="user-name">
              {{ infoFormState.name }}
            </span>

            <el-text>{{ infoFormState.roles?.map((item) => item.name).join("、") }}</el-text>
          </div>

          <el-divider />

          <el-descriptions :column="1" border>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <User />
                  </el-icon>
                  <span>账号</span>
                </div>
              </template>
              <span>{{ infoFormState.username }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <Coordinate />
                  </el-icon>
                  <span>部门</span>
                </div>
              </template>
              <span>{{ infoFormState.dept?.name }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <OfficeBuilding />
                  </el-icon>
                  <span>岗位</span>
                </div>
              </template>
              <span>{{ infoFormState.positions?.map((item) => item.name).join("、") }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <Phone />
                  </el-icon>
                  <span>手机</span>
                </div>
              </template>
              <span>{{ infoFormState.mobile }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <Message />
                  </el-icon>
                  <span>邮箱</span>
                </div>
              </template>
              <span>{{ infoFormState.email }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <Clock />
                  </el-icon>
                  <span>加入时间</span>
                </div>
              </template>
              <span>{{ infoFormState.created_time }}</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <!-- 右侧设置区域 -->
      <el-col :span="18" class="mb-4">
        <el-card :loading="loading" shadow="hover">
          <el-tabs type="border-card">
            <el-tab-pane>
              <template #label>
                <el-icon>
                  <User />
                </el-icon>
                <span>基本设置</span>
              </template>
              <div>
                <el-form
                  ref="infoFormRef"
                  :model="infoFormState"
                  :rules="rules"
                  label-width="80px"
                  label-suffix=":"
                >
                  <el-form-item label="用户名" prop="name">
                    <el-input
                      v-model="infoFormState.name"
                      placeholder="请输入用户名"
                      prefix-icon="User"
                      clearable
                      style="width: 240px"
                    />
                  </el-form-item>

                  <el-form-item label="手机号" prop="mobile">
                    <el-input
                      v-model="infoFormState.mobile"
                      placeholder="请输入手机号码"
                      prefix-icon="Phone"
                      clearable
                      style="width: 240px"
                    />
                  </el-form-item>

                  <el-form-item label="邮箱" prop="email">
                    <el-input
                      v-model="infoFormState.email"
                      placeholder="请输入邮箱"
                      prefix-icon="Message"
                      clearable
                      style="width: 240px"
                    />
                  </el-form-item>

                  <el-form-item label="性别" prop="gender">
                    <el-radio-group v-model="infoFormState.gender">
                      <el-radio
                        v-for="item in dictDataStore['sys_user_sex']"
                        :key="item.dict_value"
                        :value="item.dict_value"
                      >
                        {{ item.dict_label }}
                      </el-radio>
                    </el-radio-group>
                  </el-form-item>

                  <el-form-item>
                    <el-button
                      type="primary"
                      :loading="infoSubmitting"
                      icon="edit"
                      @click="handleSave"
                    >
                      保存更改
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>

            <el-tab-pane>
              <template #label>
                <el-icon>
                  <Lock />
                </el-icon>
                <span>安全设置</span>
              </template>
              <div>
                <el-form
                  ref="passwordFormRef"
                  :model="passwordFormState"
                  :rules="resetPasswordRules"
                  label-width="120px"
                  label-suffix=":"
                >
                  <el-form-item label="当前密码" prop="old_password">
                    <el-input
                      v-model.trim="passwordFormState.old_password"
                      :placeholder="t('login.password')"
                      type="password"
                      prefix-icon="Unlock"
                      show-password
                      clearable
                      style="width: 240px"
                    >
                      <template #prefix>
                        <Lock />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="新密码" prop="new_password">
                    <el-input
                      v-model.trim="passwordFormState.new_password"
                      type="password"
                      :placeholder="t('login.newPassword')"
                      prefix-icon="Unlock"
                      show-password
                      clearable
                      style="width: 240px"
                    >
                      <template #prefix>
                        <Key />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="确认新密码" prop="confirm_password">
                    <el-input
                      v-model.trim="passwordFormState.confirm_password"
                      type="password"
                      :placeholder="t('login.message.password.confirm')"
                      prefix-icon="Lock"
                      show-password
                      clearable
                      style="width: 240px"
                    >
                      <template #prefix>
                        <Check />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item>
                    <el-button
                      type="primary"
                      :loading="passwordChanging"
                      icon="edit"
                      @click="handlePasswordChange"
                    >
                      更新密码
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import type {
  FormInstance,
  UploadRequestOptions,
  UploadFile,
  ElUpload,
  ComponentSize,
} from "element-plus";
import UserAPI, { type InfoFormState, type PasswordFormState } from "@/api/module_system/user";
import { useUserStore, useDictStore } from "@/store";
import { useUserStoreHook } from "@/store/modules/user.store";
import { Camera } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { useI18n } from "vue-i18n";
import { nextTick } from "vue";
import router from "@/router";

const { t } = useI18n();
const userStore = useUserStore();
const dictStore = useDictStore();
const infoFormRef = ref<FormInstance>();
const passwordFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);

const dictDataStore = computed(() => dictStore.dictData);

const size = ref<ComponentSize>("default");

const iconStyle = computed(() => {
  const marginMap = {
    large: "8px",
    default: "6px",
    small: "4px",
  };
  return {
    marginRight: marginMap[size.value || "default"],
  };
});

// 字典数据
const getOptions = async () => {
  return await dictStore.getDict(["sys_user_sex"]);
};

// 状态定义
const passwordChanging = ref(false);
const infoSubmitting = ref(false);

// 用户基础信息表单
const infoFormState = reactive<InfoFormState>({
  name: undefined,
  gender: 1,
  mobile: undefined,
  email: undefined,
  username: undefined,
  dept_name: undefined,
  dept: {},
  positions: [],
  roles: [],
  avatar: undefined,
  created_time: undefined,
});

// 修改密码表单
const passwordFormState = reactive<PasswordFormState>({
  old_password: "",
  new_password: "",
  confirm_password: "",
});

// 头像上传处理优化
const fileList = ref<any[]>([]);
const uploadRef = ref<InstanceType<typeof ElUpload>>();

// 文件上传前校验
const handleBeforeUpload = (file: File) => {
  const isImage = file.type.startsWith("image/");
  const isLt2M = file.size / 1024 / 1024 < 2;

  if (!isImage) {
    ElMessage.error("只能上传图片文件");
    return false;
  }
  if (!isLt2M) {
    ElMessage.error("上传图片大小不能超过 2MB!");
    return false;
  }
  return true;
};

// 自定义上传处理
const handleUpload = async (options: UploadRequestOptions) => {
  try {
    const file = options.file;
    const formData = new FormData();
    formData.append("file", file);

    const response = await UserAPI.uploadCurrentUserAvatar(formData);

    if (response.data.code === 0 && response.data.data) {
      const fileUrl = response.data.data.file_url;
      updateAvatar(fileUrl);
      options.onSuccess(response);
      // 重置上传组件状态，允许再次选择上传
      if (uploadRef.value) {
        uploadRef.value.clearFiles();
      }
      fileList.value = [];
    } else {
      const errorMsg = response.data.msg || "上传失败";
      ElMessage.error(errorMsg);
      options.onError({
        ...new Error(errorMsg),
        status: response.status || 500,
        method: "POST",
        url: "/system/user/current/avatar/upload",
      });
    }
  } catch (error) {
    ElMessage.error("头像上传失败，请重试");
    const errorObj = error instanceof Error ? error : new Error(String(error));
    options.onError({
      ...errorObj,
      status: 500,
      method: "POST",
      url: "/system/user/current/avatar/upload",
    });
    console.error("Upload error:", error);
  }
};

// 处理文件选择变化
const handleFileChange = (file: UploadFile, files: UploadFile[]) => {
  // 当有新文件被添加且状态为ready时触发上传
  if (file) {
    // 更新文件列表
    fileList.value = [...files];
    // 提交上传
    if (uploadRef.value) {
      uploadRef.value.submit();
    }
  }
};

// 更新头像信息
const updateAvatar = (fileUrl: string) => {
  if (fileUrl) {
    // 更新头像状态
    infoFormState.avatar = fileUrl;
    // 确保DOM正确更新
    nextTick(() => {
      console.log("头像已更新:", infoFormState.avatar);
    });
  } else {
    ElMessage.error("无效的头像URL");
    console.error("Invalid fileUrl:", fileUrl);
  }
};

// 邮箱校验规则优化
const rules = {
  name: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  mobile: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: "请输入有效的手机号格式",
      trigger: "blur",
    },
  ],
  email: [
    {
      pattern: /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/,
      message: "请输入有效的邮箱格式",
      trigger: "blur",
    },
  ],
};

const resetPasswordRules = {
  old_password: [
    {
      required: true,
      trigger: "blur",
      message: t("login.password"),
    },
  ],
  new_password: [
    {
      required: true,
      trigger: "blur",
      message: t("login.message.password.required"),
    },
    {
      min: 6,
      message: t("login.message.password.min"),
      trigger: "blur",
    },
  ],
  confirm_password: [
    {
      required: true,
      trigger: "blur",
      message: t("login.message.password.required"),
    },
    {
      min: 6,
      message: t("login.message.password.min"),
      trigger: "blur",
    },
    {
      validator: (_: any, value: string) => {
        return value === passwordFormState.new_password;
      },
      trigger: "blur",
      message: t("login.message.password.inconformity"),
    },
  ],
};

// 初始化表单
const initInfoForm = () => {
  const basicInfo = userStore.basicInfo;
  Object.assign(infoFormState, { ...basicInfo });
};

// 初始化密码表单
const initPasswordForm = () => {
  Object.assign(passwordFormState, {
    old_password: "",
    new_password: "",
    confirm_password: "",
  });
};

// 基本信息表单提交
const handleSave = async () => {
  try {
    infoSubmitting.value = true;
    const valid = await infoFormRef.value?.validate().catch(() => false);
    if (!valid) {
      return;
    }
    // 确保avatar字段被正确处理
    const response = await UserAPI.updateCurrentUserInfo({ ...infoFormState });
    await userStore.setUserInfo(response.data.data);
    ElMessage.success("个人资料已保存");
  } finally {
    infoSubmitting.value = false;
  }
};

// 修改密码
const handlePasswordChange = async () => {
  try {
    passwordChanging.value = true;
    const valid = await passwordFormRef.value?.validate().catch(() => false);
    if (!valid) {
      return;
    }
    const response = await UserAPI.changeCurrentUserPassword(passwordFormState);
    initPasswordForm();
    await redirectToLogin(response.data.msg);
  } catch (error) {
    console.error(error);
  } finally {
    passwordChanging.value = false;
  }
};

/**
 * 重定向到登录页面
 */
async function redirectToLogin(message: string = "请重新登录"): Promise<void> {
  try {
    ElNotification({
      title: "提示",
      message,
      type: "warning",
      duration: 3000,
    });

    await useUserStoreHook().resetAllState();

    // 跳转到登录页，保留当前路由用于登录后跳转
    const currentPath = router.currentRoute.value.fullPath;
    await router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
  } catch (error: any) {
    console.error(error);
  }
}

onMounted(async () => {
  await getOptions();
  initInfoForm();
});
</script>

<style lang="scss" scoped>
/* 样式调整 */
.user-info-header {
  display: flex;
  flex-direction: column;
  align-items: center;

  .avatar-wrapper {
    position: relative;
    margin-bottom: 16px;

    .el-upload {
      &:hover {
        opacity: 0.8; /* 鼠标悬浮时稍微降低透明度 */
      }
    }

    .upload-trigger {
      // top: 50%;
      // left: 50%;
      position: absolute;
      width: 28px;
      height: 28px;
      background: var(--el-color-primary);
      border-radius: 50%;
      opacity: 0;
      transform: translate(-50%, -50%);
    }

    /* 提升 hover 样式优先级 */
    &:hover .upload-trigger {
      opacity: 1 !important; /* 强制生效 */
    }
  }
}

/* 修复表单输入框清除按钮导致的宽度变化问题 */
.el-input {
  transition: none !important;
}

.el-input__wrapper {
  transition: none !important;
}

.iconStyle {
  margin-right: 6px;
}

.cell-item {
  display: flex;
  align-items: center;
}
</style>
