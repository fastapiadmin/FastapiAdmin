<!-- 参数配置 -->
<template>
  <FaDrawer
    v-model="drawerVisible"
    title="配置中心"
    :size="drawerSize"
    destroy-on-close
    @close="onDrawerClosed"
  >
    <ElTabs v-model="activeTabRef" type="border-card">
      <!-- 网站配置 -->
      <ElTabPane label="网站配置" name="website">
        <ElForm :model="configState" label-suffix=":" label-width="100px" label-position="right">
          <!-- 系统配置 -->
          <ElDivider>网站配置</ElDivider>
          <div v-for="(item, key) in systemConfigs" :key="key">
            <ElFormItem :label="item.config_name">
              <span class="flex items-center gap-2 w-full">
                <ElInput
                  v-model="item.config_value"
                  :placeholder="t('common.inputText')"
                  clearable
                  :style="'width: 100%'"
                  @input="markModified(key)"
                />
              </span>
            </ElFormItem>
          </div>

          <!-- logo配置 -->
          <ElDivider>网站图标</ElDivider>
          <div v-for="(item, key) in logoConfigs" :key="key">
            <ElFormItem :label="item.config_name">
              <div class="flex items-center gap-2 w-full">
                <SingleImageUpload
                  v-model="item.config_value"
                  :data="{ type: key }"
                  :name="'file'"
                  :max-file-size="item.maxFileSize"
                  :show-tip="true"
                  :enable-preview="true"
                  :enable-crop="true"
                  v-bind="logoCropBind(String(key))"
                  @success="(fileInfo: UploadFilePath) => handleUploadSuccess(fileInfo, key)"
                  @error="handleUploadError"
                />
              </div>
            </ElFormItem>
          </div>
        </ElForm>
      </ElTabPane>
      <ElTabPane label="安全隐私" name="securityPrivacy">
        <ElForm :model="configState" label-suffix=":" label-width="100px" label-position="right">
          <!-- 系统配置 -->
          <ElDivider>安全隐私</ElDivider>
          <div v-for="(item, key) in securityPrivacyConfigs" :key="key">
            <ElFormItem :label="item.config_name">
              <span class="flex items-center gap-2 w-full">
                <ElInput
                  v-model="item.config_value"
                  :placeholder="t('common.inputText')"
                  clearable
                  :style="'width: 100%'"
                  @input="markModified(key)"
                />
              </span>
            </ElFormItem>
          </div>
        </ElForm>
      </ElTabPane>
      <ElTabPane label="用户协议" name="userAgreement">
        <!-- 系统配置 -->
        <ElForm :model="configState" label-suffix=":" label-width="100px" label-position="right">
          <ElDivider>用户协议</ElDivider>
          <div v-for="(item, key) in userAgreementConfigs" :key="key">
            <ElFormItem :label="item.config_name">
              <span class="flex items-center gap-2 w-full">
                <ElInput
                  v-model="item.config_value"
                  :placeholder="t('common.inputText')"
                  clearable
                  :style="'width: 100%'"
                  @input="markModified(key)"
                />
              </span>
            </ElFormItem>
          </div>
        </ElForm>
      </ElTabPane>
      <ElTabPane label="接口白名单" name="apiWhitelist">
        <ElForm :model="configState" label-suffix=":" label-width="100px" label-position="right">
          <!-- 系统配置 -->
          <ElDivider>接口白名单</ElDivider>
          <div v-for="(item, key) in apiWhitelistConfigs" :key="key">
            <ElFormItem :label="item.config_name">
              <div class="space-y-2">
                <div
                  v-for="listItem in apiWhitelistItems"
                  :key="listItem.id"
                  class="flex items-center gap-2"
                >
                  <ElInput
                    v-model="listItem.value"
                    :placeholder="'/api/v1/users/get'"
                    clearable
                    @input="markModified(key)"
                    @blur="
                      {
                        if (!isValidApiPath(listItem.value) && listItem.value.trim()) {
                          ElMessage.warning('请输入有效的接口路径格式（以/开头）');
                        }
                      }
                    "
                  />
                  <ElButton
                    type="danger"
                    icon="minus"
                    circle
                    size="small"
                    @click="removeApiWhitelistItem(listItem.id)"
                  />
                </div>
                <ElButton
                  type="primary"
                  icon="plus"
                  size="small"
                  :style="'margin-top: 10px'"
                  @click="addApiWhitelistItem"
                >
                  添加接口路径
                </ElButton>
                <div class="text-xs text-gray-500 mt-2">
                  配置说明：添加到白名单的接口路径无需登录即可访问，支持完整路径配置。
                </div>
              </div>
            </ElFormItem>
          </div>
        </ElForm>
      </ElTabPane>
      <ElTabPane label="IP黑名单" name="ipBlacklist">
        <ElForm :model="configState" label-suffix=":" label-width="100px" label-position="right">
          <!-- 系统配置 -->
          <ElDivider>IP黑名单</ElDivider>
          <div v-for="(item, key) in ipBlacklistConfigs" :key="key">
            <ElFormItem :label="item.config_name">
              <div class="space-y-2">
                <div
                  v-for="listItem in ipBlacklistItems"
                  :key="listItem.id"
                  class="flex items-center gap-2"
                >
                  <ElInput
                    v-model="listItem.value"
                    :placeholder="'192.168.1.1'"
                    clearable
                    :style="'flex: 1'"
                    @input="markModified(key)"
                    @blur="
                      {
                        if (!isValidIp(listItem.value) && listItem.value.trim()) {
                          ElMessage.warning('请输入有效的IP地址格式');
                        }
                      }
                    "
                  />
                  <ElButton
                    type="danger"
                    icon="minus"
                    circle
                    size="small"
                    @click="removeIpBlacklistItem(listItem.id)"
                  />
                </div>
                <ElButton
                  type="primary"
                  icon="plus"
                  size="small"
                  :style="'margin-top: 10px'"
                  @click="addIpBlacklistItem"
                >
                  添加IP地址
                </ElButton>
                <div class="text-xs text-gray-500 mt-2">
                  配置说明：添加到黑名单的IP地址将无法访问系统，支持单个IP配置。
                </div>
              </div>
            </ElFormItem>
          </div>
        </ElForm>
      </ElTabPane>
      <ElTabPane label="演示环境配置" name="demo">
        <ElForm :model="configState" label-suffix=":" label-width="100px" label-position="right">
          <!-- 系统配置 -->
          <ElDivider>演示环境配置</ElDivider>
          <div v-for="(item, key) in demoConfigs" :key="key">
            <ElFormItem :label="item.config_name">
              <!-- 演示模式开关 -->
              <template v-if="key === 'demo_enable'">
                <ElSwitch
                  inline-prompt
                  active-text="启用"
                  inactive-text="禁用"
                  :model-value="item.config_value === 'true'"
                  @update:model-value="
                    (value) => {
                      item.config_value = value ? 'true' : 'false';
                      markModified(key);
                    }
                  "
                />
                <div class="text-xs text-gray-500 mt-1">
                  配置说明：启用后系统将进入演示模式，部分功能可能受限。
                </div>
              </template>
              <!-- IP白名单 -->
              <template v-else-if="key === 'ip_white_list'">
                <div class="space-y-2">
                  <div
                    v-for="listItem in demoIpWhitelistItems"
                    :key="listItem.id"
                    class="flex items-center gap-2"
                  >
                    <ElInput
                      v-model="listItem.value"
                      :placeholder="'192.168.1.1'"
                      clearable
                      :style="'flex: 1'"
                      @input="markModified(key)"
                      @blur="
                        {
                          if (!isValidIp(listItem.value) && listItem.value.trim()) {
                            ElMessage.warning('请输入有效的IP地址格式');
                          }
                        }
                      "
                    />
                    <ElButton
                      type="danger"
                      icon="minus"
                      circle
                      size="small"
                      @click="removeDemoIpWhitelistItem(listItem.id)"
                    />
                  </div>
                  <ElButton
                    type="primary"
                    icon="plus"
                    size="small"
                    :style="'margin-top: 10px'"
                    @click="addDemoIpWhitelistItem"
                  >
                    添加IP地址
                  </ElButton>
                  <div class="text-xs text-gray-500 mt-2">
                    配置说明：演示模式下，只有白名单中的IP地址可以访问系统，支持单个IP配置。
                  </div>
                </div>
              </template>
              <!-- 其他配置项 -->
              <template v-else>
                <ElInput
                  v-model="item.config_value"
                  :placeholder="t('common.inputText')"
                  clearable
                  :style="'width: 100%'"
                  @input="markModified(key)"
                />
              </template>
            </ElFormItem>
          </div>
        </ElForm>
      </ElTabPane>
    </ElTabs>
    <template #footer>
      <ElButton @click="handleCloseDialog">取消</ElButton>
      <ElButton
        v-hasPerm="['module_system:config:update']"
        type="primary"
        :disabled="!hasChanges"
        @click="submitChanges"
      >
        保存
      </ElButton>
    </template>
  </FaDrawer>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, computed } from "vue";
import ParamsAPI, { type ConfigTable } from "@/api/module_system/params";
import { useConfigStore } from "@stores";
import { useI18n } from "vue-i18n";
import { ElMessage, ElMessageBox } from "element-plus";
import FaDrawer from "@/components/modal/fa-drawer/index.vue";
import SingleImageUpload from "@/components/others/fa-upload/index.vue";
import { useAppStore } from "@stores/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

// 定义列表项类型
interface ListItem {
  id: string;
  value: string;
}

// 生成唯一ID
const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};

// IP地址验证函数
const isValidIp = (ip: string): boolean => {
  const ipRegex =
    /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return ipRegex.test(ip);
};

// 接口路径验证函数
const isValidApiPath = (path: string): boolean => {
  const pathRegex = /^\/[\w\-/]+$/;
  return pathRegex.test(path);
};

const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "60%" : "60%"));

const t = useI18n().t;
const configStore = useConfigStore();

/** 网站图标裁剪：favicon 方形、Logo 横版、登录背景 16:9 */
function logoCropBind(key: string) {
  switch (key) {
    case "sys_web_favicon":
      return {
        cropCutWidth: 64,
        cropCutHeight: 64,
        cropBoxWidth: 380,
        cropBoxHeight: 320,
        cropDialogTitle: "裁剪网站图标",
        cropInnerTitle: "调整图标",
        cropPreviewTitle: "预览",
      };
    case "sys_web_logo":
      return {
        cropCutWidth: 320,
        cropCutHeight: 96,
        cropBoxWidth: 520,
        cropBoxHeight: 360,
        cropDialogTitle: "裁剪站点 Logo",
        cropInnerTitle: "调整 Logo",
        cropPreviewTitle: "预览",
      };
    case "sys_login_background":
      return {
        cropCutWidth: 960,
        cropCutHeight: 540,
        cropBoxWidth: 560,
        cropBoxHeight: 380,
        cropDialogTitle: "裁剪登录背景",
        cropInnerTitle: "调整背景图",
        cropPreviewTitle: "预览",
        cropFileType: "jpeg" as const,
      };
    default:
      return {};
  }
}
const activeTabRef = ref("website");

// 与父组件的 v-model 同步
const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits(["update:modelValue"]);
const drawerVisible = computed({
  get: () => props.modelValue,
  set: (val: boolean) => emit("update:modelValue", val),
});

// 配置状态管理
const configState = reactive<ConfigTable>({
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: undefined,
  description: "",
});

// 记录修改过的字段
const modifiedFields = reactive<Record<string, boolean>>({});

// 标记字段为已修改
const markModified = (key: string) => {
  modifiedFields[key] = true;
};

// 判断是否有修改
const hasChanges = computed(() => Object.keys(modifiedFields).length > 0);

// 提交修改
const submitChanges = async () => {
  const keysToSubmit = Object.keys(modifiedFields);
  if (keysToSubmit.length === 0) return;

  try {
    // 准备提交数据
    // 1. 处理接口白名单
    if (
      "white_api_list_path" in modifiedFields &&
      apiWhitelistConfigs.value.white_api_list_path?.id
    ) {
      const apiWhitelistArray = apiWhitelistItems.value
        .map((item) => item.value.trim())
        .filter(Boolean);
      // 转换为JSON字符串格式保存
      const apiWhitelistJson = JSON.stringify(apiWhitelistArray);
      await ParamsAPI.updateParams(apiWhitelistConfigs.value.white_api_list_path.id, {
        ...apiWhitelistConfigs.value.white_api_list_path,
        config_value: apiWhitelistJson,
      });
    }

    // 2. 处理IP黑名单
    if ("ip_black_list" in modifiedFields && ipBlacklistConfigs.value.ip_black_list?.id) {
      const ipBlacklistArray = ipBlacklistItems.value
        .map((item) => item.value.trim())
        .filter(Boolean);
      // 转换为JSON字符串格式保存
      const ipBlacklistJson = JSON.stringify(ipBlacklistArray);
      await ParamsAPI.updateParams(ipBlacklistConfigs.value.ip_black_list.id, {
        ...ipBlacklistConfigs.value.ip_black_list,
        config_value: ipBlacklistJson,
      });
    }

    // 3. 处理演示环境IP白名单
    if ("ip_white_list" in modifiedFields && demoConfigs.value.ip_white_list?.id) {
      const demoIpWhitelistArray = demoIpWhitelistItems.value
        .map((item) => item.value.trim())
        .filter(Boolean);
      // 转换为JSON字符串格式保存
      const demoIpWhitelistJson = JSON.stringify(demoIpWhitelistArray);
      await ParamsAPI.updateParams(demoConfigs.value.ip_white_list.id, {
        ...demoConfigs.value.ip_white_list,
        config_value: demoIpWhitelistJson,
      });
    }

    // 4. 处理其他配置项
    const otherKeys = keysToSubmit.filter(
      (key) => !["white_api_list_path", "ip_black_list", "ip_white_list"].includes(key)
    );
    const otherUpdatePromises = otherKeys.map((key) => {
      const item =
        systemConfigs.value[key as keyof typeof systemConfigs.value] ||
        logoConfigs.value[key as keyof typeof logoConfigs.value] ||
        securityPrivacyConfigs.value[key as keyof typeof securityPrivacyConfigs.value] ||
        userAgreementConfigs.value[key as keyof typeof userAgreementConfigs.value] ||
        demoConfigs.value[key as keyof typeof demoConfigs.value];
      return item && item.id ? ParamsAPI.updateParams(item.id, { ...item }) : Promise.resolve();
    });
    await Promise.all(otherUpdatePromises);

    // 清除已提交的修改标记
    keysToSubmit.forEach((key) => {
      delete modifiedFields[key];
    });

    // 重新加载配置数据（强制重新加载以同步到浏览器内存）
    configStore.isConfigLoaded = false;
    await configStore.getConfig();
    initializeLists();
  } catch (error) {
    console.error("保存失败:", error);
  }
};

// 取消修改：重置所有修改字段的状态并恢复初始值
const resetForm = async () => {
  // 强制重新加载配置数据（从服务器获取最新数据）
  await configStore.getConfig(true);

  // 重置动态列表
  initializeLists();

  // 重置其他配置项
  const keysToReset = Object.keys(modifiedFields);
  for (const key of keysToReset) {
    if (systemConfigs.value[key as keyof typeof systemConfigs.value]) {
      systemConfigs.value[key as keyof typeof systemConfigs.value].config_value =
        configStore.configData[key as keyof typeof configStore.configData]?.config_value || "";
    } else if (logoConfigs.value[key as keyof typeof logoConfigs.value]) {
      logoConfigs.value[key as keyof typeof logoConfigs.value].config_value =
        configStore.configData[key as keyof typeof configStore.configData]?.config_value || "";
    } else if (securityPrivacyConfigs.value[key as keyof typeof securityPrivacyConfigs.value]) {
      securityPrivacyConfigs.value[key as keyof typeof securityPrivacyConfigs.value].config_value =
        configStore.configData[key as keyof typeof configStore.configData]?.config_value || "";
    } else if (userAgreementConfigs.value[key as keyof typeof userAgreementConfigs.value]) {
      userAgreementConfigs.value[key as keyof typeof userAgreementConfigs.value].config_value =
        configStore.configData[key as keyof typeof configStore.configData]?.config_value || "";
    } else if (demoConfigs.value[key as keyof typeof demoConfigs.value]) {
      // 除了IP白名单外的演示配置项
      if (key !== "ip_white_list") {
        demoConfigs.value[key as keyof typeof demoConfigs.value].config_value =
          configStore.configData[key as keyof typeof configStore.configData]?.config_value || "";
      }
    }
    delete modifiedFields[key];
  }
  ElMessageBox.close();
};

async function handleCloseDialog() {
  // 仅关闭抽屉，等待关闭动画结束后再重置
  drawerVisible.value = false;
}

async function onDrawerClosed() {
  // 抽屉关闭动画结束后再执行重置，避免打断动画
  await resetForm();
}

// 系统配置项
const systemConfigs = computed(() => ({
  sys_web_title: configStore.configData.sys_web_title,
  sys_web_version: configStore.configData.sys_web_version,
  sys_web_description: configStore.configData.sys_web_description,
}));

// 安全隐私配置项
const securityPrivacyConfigs = computed(() => ({
  sys_help_doc: configStore.configData.sys_help_doc,
  sys_git_code: configStore.configData.sys_git_code,
  sys_keep_record: configStore.configData.sys_keep_record,
  sys_web_copyright: configStore.configData.sys_web_copyright,
  sys_web_privacy: configStore.configData.sys_web_privacy,
}));

// 用户协议配置项
const userAgreementConfigs = computed(() => ({
  sys_web_clause: configStore.configData.sys_web_clause,
}));

// 接口白名单配置 - 动态管理
const apiWhitelistItems = ref<ListItem[]>([]);
// IP黑名单配置 - 动态管理
const ipBlacklistItems = ref<ListItem[]>([]);
// IP白名单配置 - 动态管理
const demoIpWhitelistItems = ref<ListItem[]>([]);

// 从配置数据初始化列表
const initializeLists = () => {
  // 初始化接口白名单
  const apiWhitelistStr = configStore.configData.white_api_list_path?.config_value || "";
  try {
    // 尝试解析为JSON数组
    const apiWhitelistArray = JSON.parse(apiWhitelistStr);
    if (Array.isArray(apiWhitelistArray)) {
      apiWhitelistItems.value = apiWhitelistArray
        .filter((item) => typeof item === "string" && item.trim())
        .map((item) => ({ id: generateId(), value: item.trim() }));
    } else {
      // 如果不是数组，回退到按换行符分割
      apiWhitelistItems.value = apiWhitelistStr
        ? apiWhitelistStr
            .split("\n")
            .filter((item) => item.trim())
            .map((item) => ({ id: generateId(), value: item.trim() }))
        : [{ id: generateId(), value: "" }];
    }
  } catch {
    // 解析失败，回退到按换行符分割
    apiWhitelistItems.value = apiWhitelistStr
      ? apiWhitelistStr
          .split("\n")
          .filter((item) => item.trim())
          .map((item) => ({ id: generateId(), value: item.trim() }))
      : [{ id: generateId(), value: "" }];
  }

  // 初始化IP黑名单
  const ipBlacklistStr = configStore.configData.ip_black_list?.config_value || "";
  try {
    // 尝试解析为JSON数组
    const ipBlacklistArray = JSON.parse(ipBlacklistStr);
    if (Array.isArray(ipBlacklistArray)) {
      ipBlacklistItems.value = ipBlacklistArray
        .filter((item) => typeof item === "string" && item.trim())
        .map((item) => ({ id: generateId(), value: item.trim() }));
    } else {
      // 如果不是数组，回退到按换行符分割
      ipBlacklistItems.value = ipBlacklistStr
        ? ipBlacklistStr
            .split("\n")
            .filter((item) => item.trim())
            .map((item) => ({ id: generateId(), value: item.trim() }))
        : [{ id: generateId(), value: "" }];
    }
  } catch {
    // 解析失败，回退到按换行符分割
    ipBlacklistItems.value = ipBlacklistStr
      ? ipBlacklistStr
          .split("\n")
          .filter((item) => item.trim())
          .map((item) => ({ id: generateId(), value: item.trim() }))
      : [{ id: generateId(), value: "" }];
  }

  // 初始化演示环境IP白名单
  const demoIpWhitelistStr = configStore.configData.ip_white_list?.config_value || "";
  try {
    // 尝试解析为JSON数组
    const demoIpWhitelistArray = JSON.parse(demoIpWhitelistStr);
    if (Array.isArray(demoIpWhitelistArray)) {
      demoIpWhitelistItems.value = demoIpWhitelistArray
        .filter((item) => typeof item === "string" && item.trim())
        .map((item) => ({ id: generateId(), value: item.trim() }));
    } else {
      // 如果不是数组，回退到按换行符分割
      demoIpWhitelistItems.value = demoIpWhitelistStr
        ? demoIpWhitelistStr
            .split("\n")
            .filter((item) => item.trim())
            .map((item) => ({ id: generateId(), value: item.trim() }))
        : [{ id: generateId(), value: "" }];
    }
  } catch {
    // 解析失败，回退到按换行符分割
    demoIpWhitelistItems.value = demoIpWhitelistStr
      ? demoIpWhitelistStr
          .split("\n")
          .filter((item) => item.trim())
          .map((item) => ({ id: generateId(), value: item.trim() }))
      : [{ id: generateId(), value: "" }];
  }
};

// 添加接口白名单项
const addApiWhitelistItem = () => {
  apiWhitelistItems.value.push({ id: generateId(), value: "" });
  markModified("white_api_list_path");
};

// 移除接口白名单项
const removeApiWhitelistItem = (id: string) => {
  if (apiWhitelistItems.value.length <= 1) {
    ElMessage.warning("至少需要保留一个接口白名单配置");
    return;
  }
  apiWhitelistItems.value = apiWhitelistItems.value.filter((item) => item.id !== id);
  markModified("white_api_list_path");
};

// 添加IP黑名单项
const addIpBlacklistItem = () => {
  ipBlacklistItems.value.push({ id: generateId(), value: "" });
  markModified("ip_black_list");
};

// 移除IP黑名单项
const removeIpBlacklistItem = (id: string) => {
  if (ipBlacklistItems.value.length <= 1) {
    ElMessage.warning("至少需要保留一个IP黑名单配置");
    return;
  }
  ipBlacklistItems.value = ipBlacklistItems.value.filter((item) => item.id !== id);
  markModified("ip_black_list");
};

// 添加演示环境IP白名单项
const addDemoIpWhitelistItem = () => {
  demoIpWhitelistItems.value.push({ id: generateId(), value: "" });
  markModified("ip_white_list");
};

// 移除演示环境IP白名单项
const removeDemoIpWhitelistItem = (id: string) => {
  if (demoIpWhitelistItems.value.length <= 1) {
    ElMessage.warning("至少需要保留一个IP白名单配置");
    return;
  }
  demoIpWhitelistItems.value = demoIpWhitelistItems.value.filter((item) => item.id !== id);
  markModified("ip_white_list");
};

// 接口白名单配置项
const apiWhitelistConfigs = computed(() => ({
  white_api_list_path: configStore.configData.white_api_list_path,
}));

// IP黑名单配置项
const ipBlacklistConfigs = computed(() => ({
  ip_black_list: configStore.configData.ip_black_list,
}));

// 演示环境配置项
const demoConfigs = computed(() => ({
  demo_enable: configStore.configData.demo_enable,
  ip_white_list: configStore.configData.ip_white_list,
}));

// logo配置项
const logoConfigs = computed(() => ({
  sys_web_logo: {
    ...configStore.configData.sys_web_logo,
    maxFileSize: 5,
  },
  sys_web_favicon: {
    ...configStore.configData.sys_web_favicon,
    maxFileSize: 5,
  },
  sys_login_background: {
    ...configStore.configData.sys_login_background,
    maxFileSize: 10,
  },
}));

// 图片上传成功的回调处理
const handleUploadSuccess = (fileInfo: UploadFilePath, type: string) => {
  const fileUrl = fileInfo.file_url;
  if (type in configStore.configData) {
    (configStore.configData as Record<string, ConfigTable>)[type].config_value = fileUrl;
  }
  if (type in systemConfigs.value) {
    (systemConfigs.value as Record<string, { config_value: string }>)[type].config_value = fileUrl;
  } else if (type in logoConfigs.value) {
    (logoConfigs.value as Record<string, { config_value: string }>)[type].config_value = fileUrl;
  }
  markModified(type);
};

// 图片上传失败的回调处理
const handleUploadError = (error: any) => {
  console.error("上传失败:", error.message || "未知错误");
  ElMessage.error(`上传失败：${error.message || "请稍后重试"}`);
};

onMounted(() => {
  initializeLists();
  configStore.getConfig(true);
});
</script>

<style lang="scss" scoped>
.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.justify-end {
  justify-content: flex-end;
}

.gap-4 {
  gap: 1rem;
}

.mt-6 {
  margin-top: 1.5rem;
}
</style>
