<template>
  <div class="fa-full-height">
    <FaWorkbench :side-width="240">
      <template #side>
        <FaSidePanel :title="$t('common.params.groupTitle')" class="params-side">
          <button
            v-for="tab in paramTabs"
            :key="tab.name"
            type="button"
            class="params-nav-item"
            :class="{ 'is-active': activeTab === tab.name }"
            @click="activeTab = tab.name"
          >
            {{ tab.label }}
          </button>
        </FaSidePanel>
      </template>

      <div class="fa-card params-main">
        <div class="params-main__body">
          <ParamTabPane
            v-if="activeTab === 'brand'"
            :title="$t('common.params.brand')"
            :modified="brandModified"
            @save-group="saveGroup(fieldsMap.brand)"
          >
            <ParamFieldCard
              v-for="field in fieldsMap.brand"
              :key="field.key"
              :label="field.label"
              :modified="field.modified"
              @save="saveField(field)"
            >
              <FaUpload
                v-model="field.localValue"
                :style="{ width: '160px', height: '160px' }"
                :show-tip="false"
                :max-file-size="5"
                enable-crop
                @update:model-value="onFieldChange(field)"
              />
            </ParamFieldCard>
          </ParamTabPane>

          <!-- 网站信息 -->
          <ParamTabPane
            v-if="activeTab === 'website'"
            :title="$t('common.params.siteInfo')"
            :modified="websiteModified"
            @save-group="saveGroup(fieldsMap.website)"
          >
            <ParamFieldCard
              v-for="field in fieldsMap.website"
              :key="field.key"
              :label="field.label"
              :modified="field.modified"
              @save="saveField(field)"
            >
              <ElInput
                v-model="field.localValue"
                :placeholder="'输入' + field.label"
                clearable
                @input="onFieldChange(field)"
                aria-label="'输入' + field.label"
              />
            </ParamFieldCard>
          </ParamTabPane>

          <!-- 外部链接 -->
          <ParamTabPane
            v-if="activeTab === 'security'"
            :title="$t('common.params.externalLinks')"
            :modified="securityModified"
            @save-group="saveGroup(fieldsMap.security)"
          >
            <ParamFieldCard
              v-for="field in fieldsMap.security"
              :key="field.key"
              :label="field.label"
              :modified="field.modified"
              @save="saveField(field)"
            >
              <ElInput
                v-model="field.localValue"
                :placeholder="'输入' + field.label"
                clearable
                @input="onFieldChange(field)"
                aria-label="'输入' + field.label"
              />
            </ParamFieldCard>
          </ParamTabPane>

          <!-- 安全访问 -->
          <ParamTabPane
            v-if="activeTab === 'access'"
            :title="$t('common.params.security')"
            :modified="accessModified"
            @save-group="saveGroup(fieldsMap.access)"
          >
            <template v-if="fieldsMap.access.length > 0">
              <!-- IP 归属地查询 -->
              <ParamFieldCard
                :label="fieldsMap.access[0]!.label"
                :modified="fieldsMap.access[0]!.modified"
                @save="saveField(fieldsMap.access[0]!)"
              >
                <div class="flex items-center gap-3">
                  <ElSwitch
                    :model-value="fieldsMap.access[0]!.localValue === 'on'"
                    :active-text="$t('common.params.enable')"
                    :inactive-text="$t('common.params.disable')"
                    @change="(val: string | number | boolean) => onLocationChange(val === true)"
                  />
                  <span class="text-xs text-(--el-text-color-secondary)">
                    {{
                      fieldsMap.access[0]!.localValue === "on"
                        ? $t("common.params.ipLookupOn")
                        : $t("common.params.ipLookupOff")
                    }}
                  </span>
                </div>
              </ParamFieldCard>

              <!-- IP 黑名单 -->
              <ParamFieldCard
                :label="fieldsMap.access[1]!.label"
                :modified="fieldsMap.access[1]!.modified"
                @save="saveField(fieldsMap.access[1]!)"
              >
                <div class="flex flex-wrap gap-2 mb-2">
                  <ElTag
                    v-for="(ip, idx) in fieldsMap.access[1]!.ipList"
                    :key="idx"
                    type="danger"
                    closable
                    :disable-transitions="false"
                    @close="removeIp(fieldsMap.access[1]!, idx)"
                  >
                    {{ ip }}
                  </ElTag>
                  <span
                    v-if="fieldsMap.access[1]!.ipList.length === 0"
                    class="text-xs text-(--el-text-color-placeholder) leading-8"
                    >{{ $t("common.params.noIp") }}</span
                  >
                </div>
                <div class="flex gap-2">
                  <ElInput
                    v-model="fieldsMap.access[1]!.newIp"
                    :placeholder="$t('common.params.ipPlaceholder')"
                    size="small"
                    class="w-48!"
                    @keyup.enter="addIp(fieldsMap.access[1]!)"
                    :aria-label="$t('common.params.ipPlaceholder')"
                  />
                  <ElButton
                    size="small"
                    type="primary"
                    :disabled="!fieldsMap.access[1]!.newIp.trim()"
                    @click="addIp(fieldsMap.access[1]!)"
                    >{{ $t("common.params.add") }}</ElButton
                  >
                </div>
              </ParamFieldCard>
            </template>
          </ParamTabPane>

          <!-- 演示环境 -->
          <ParamTabPane
            v-if="activeTab === 'demo'"
            :title="$t('common.params.demoEnv')"
            :modified="demoModified"
            @save-group="saveGroup(fieldsMap.demo)"
          >
            <template v-if="fieldsMap.demo.length > 0">
              <!-- 演示模式 -->
              <ParamFieldCard
                :label="fieldsMap.demo[0]!.label"
                :modified="fieldsMap.demo[0]!.modified"
                @save="saveField(fieldsMap.demo[0]!)"
              >
                <div class="flex items-center gap-3">
                  <ElSwitch
                    :model-value="fieldsMap.demo[0]!.localValue === 'on'"
                    :active-text="$t('common.params.enable')"
                    :inactive-text="$t('common.params.disable')"
                    @change="(val: string | number | boolean) => onDemoChange(val === true)"
                  />
                  <span class="text-xs text-(--el-text-color-secondary)">
                    {{
                      fieldsMap.demo[0]!.localValue === "on"
                        ? "演示模式已开启，非白名单 IP 仅允许 GET 请求"
                        : "演示模式已关闭，所有功能正常访问"
                    }}
                  </span>
                </div>
              </ParamFieldCard>

              <!-- IP 白名单 -->
              <ParamFieldCard
                :label="fieldsMap.demo[1]!.label"
                :modified="fieldsMap.demo[1]!.modified"
                @save="saveField(fieldsMap.demo[1]!)"
              >
                <div class="flex flex-wrap gap-2 mb-2">
                  <ElTag
                    v-for="(ip, idx) in fieldsMap.demo[1]!.ipList"
                    :key="idx"
                    type="success"
                    closable
                    :disable-transitions="false"
                    @close="removeIp(fieldsMap.demo[1]!, idx)"
                  >
                    {{ ip }}
                  </ElTag>
                  <span
                    v-if="fieldsMap.demo[1]!.ipList.length === 0"
                    class="text-xs text-(--el-text-color-placeholder) leading-8"
                    >{{ $t("common.params.noIp") }}</span
                  >
                </div>
                <div class="flex gap-2">
                  <ElInput
                    v-model="fieldsMap.demo[1]!.newIp"
                    :placeholder="$t('common.params.ipPlaceholder')"
                    size="small"
                    class="w-48!"
                    @keyup.enter="addIp(fieldsMap.demo[1]!)"
                    :aria-label="$t('common.params.ipPlaceholder')"
                  />
                  <ElButton
                    size="small"
                    type="primary"
                    :disabled="!fieldsMap.demo[1]!.newIp.trim()"
                    @click="addIp(fieldsMap.demo[1]!)"
                    >{{ $t("common.params.add") }}</ElButton
                  >
                </div>
              </ParamFieldCard>
            </template>
          </ParamTabPane>
        </div>

        <div v-if="modifiedCount > 0" class="param-save-bar">
          <span class="param-save-bar__text">有 {{ modifiedCount }} 项修改未保存</span>
          <ElButton type="primary" :loading="saveAllLoading" @click="saveAll">保存全部</ElButton>
        </div>
      </div>
    </FaWorkbench>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from "element-plus";
import ParamsAPI from "@/api/module_system/params";
import { useConfigStore } from "@stores";
import ParamTabPane from "./components/ParamTabPane.vue";
import ParamFieldCard from "./components/ParamFieldCard.vue";

// 与菜单 route_name 一致：KeepAlive 的 include/exclude 按组件 name 匹配
defineOptions({ name: "Params" });

const configStore = useConfigStore();
const activeTab = ref("brand");

const paramTabs = [
  { name: "brand", label: "品牌标识" },
  { name: "website", label: "网站信息" },
  { name: "security", label: "外部链接" },
  { name: "access", label: "访问控制" },
  { name: "demo", label: "演示环境" },
];

// ─── 字段类型 ───

interface ParamField {
  key: string;
  label: string;
  localValue: string;
  displayValue: string;
  id?: number;
  configName?: string;
  configKey?: string;
  ipList: string[];
  newIp: string;
  modified: boolean;
}

// ─── 工具函数 ───

function buildField(key: string, label: string): ParamField {
  const param = configStore.configData[key];
  const raw = param?.config_value ?? "";
  const display = typeof raw === "string" && raw.trim() ? raw.trim() : "";
  let ipArr: string[] = [];
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) ipArr = parsed;
    } catch {
      // 不是 JSON 数组，当纯文本处理
    }
  }
  return {
    key,
    label,
    localValue: display,
    displayValue: display,
    id: param?.id,
    configName: param?.config_name,
    configKey: param?.config_key,
    ipList: ipArr,
    newIp: "",
    modified: false,
  };
}

// ─── 字段分组 ▸ 按配置项组织 ───

const fieldsMap = reactive({
  brand: [] as ParamField[],
  website: [] as ParamField[],
  security: [] as ParamField[],
  access: [] as ParamField[],
  demo: [] as ParamField[],
});

function rebuildFields() {
  fieldsMap.brand = [
    buildField("logo_url", "Logo"),
    buildField("favicon", "Favicon"),
    buildField("login_bg", "登录背景图"),
  ];
  fieldsMap.website = [
    buildField("sys_name", "系统名称"),
    buildField("login_title", "登录页标题"),
    buildField("login_subtitle", "登录页副标题"),
    buildField("version", "系统版本"),
    buildField("copyright", "版权信息"),
    buildField("keep_record", "备案号"),
    buildField("help_doc", "帮助文档地址"),
    buildField("git_code", "源码地址"),
  ];
  fieldsMap.security = [buildField("privacy", "隐私政策地址"), buildField("clause", "用户协议")];
  fieldsMap.access = [
    buildField("ip_location_enable", "IP归属地查询"),
    buildField("ip_black_list", "IP 黑名单"),
  ];
  fieldsMap.demo = [
    buildField("demo_enable", "演示模式"),
    buildField("ip_white_list", "IP 白名单"),
  ];
}

// ─── 计算 ▸ 分组是否有修改 ───

const brandModified = computed(() => fieldsMap.brand.some((f) => f.modified));
const websiteModified = computed(() => fieldsMap.website.some((f) => f.modified));
const securityModified = computed(() => fieldsMap.security.some((f) => f.modified));
const accessModified = computed(() => fieldsMap.access.some((f) => f.modified));
const demoModified = computed(() => fieldsMap.demo.some((f) => f.modified));

// ─── IP 操作 ───

function addIp(field: ParamField) {
  const ip = field.newIp.trim();
  if (!ip) return;
  if (!/^(\d{1,3}\.){3}\d{1,3}$/.test(ip)) {
    ElMessage.warning("请输入有效的 IP 地址");
    return;
  }
  if (field.ipList.includes(ip)) {
    ElMessage.info("该 IP 已存在");
    return;
  }
  field.ipList.push(ip);
  field.localValue = JSON.stringify(field.ipList);
  field.modified = true;
  field.newIp = "";
}

function removeIp(field: ParamField, index: number) {
  field.ipList.splice(index, 1);
  field.localValue = JSON.stringify(field.ipList);
  field.modified = true;
}

// ─── 保存 ───

function onFieldChange(field: ParamField) {
  field.modified = field.localValue !== field.displayValue;
}

function onDemoChange(val: boolean) {
  const field = fieldsMap.demo[0]!;
  if (!field) return;
  field.localValue = val ? "on" : "off";
  field.modified = field.localValue !== field.displayValue;
}

function onLocationChange(val: boolean) {
  const field = fieldsMap.access[0]!;
  if (!field) return;
  field.localValue = val ? "on" : "off";
  field.modified = field.localValue !== field.displayValue;
}

async function saveField(field: ParamField) {
  if (!field.id) {
    ElMessage.warning(`配置 "${field.label}" 缺少 ID，无法保存`);
    return;
  }
  if (!field.modified) {
    ElMessage.info("未检测到修改");
    return;
  }
  try {
    await ParamsAPI.updateParams(field.id, {
      config_value: field.localValue,
      config_name: field.configName,
      config_key: field.configKey,
    });
    field.modified = false;
    field.displayValue = field.localValue;
    configStore.isConfigLoaded = false;
    await configStore.getConfig();
  } catch {
    // 已由全局拦截器提示
  }
}

async function saveGroup(fields: ParamField[]) {
  const modified = fields.filter((f) => f.modified && f.id);
  if (modified.length === 0) {
    ElMessage.info("该分组无未保存的修改");
    return;
  }
  let successCount = 0;
  for (const field of modified) {
    try {
      await ParamsAPI.updateParams(
        field.id!,
        {
          config_value: field.localValue,
          config_name: field.configName,
          config_key: field.configKey,
        },
        { showSuccessMessage: false }
      );
      field.modified = false;
      field.displayValue = field.localValue;
      successCount++;
    } catch {
      // 已由全局拦截器提示
    }
  }
  if (successCount > 0) {
    configStore.isConfigLoaded = false;
    await configStore.getConfig();
    ElMessage.success(`已保存 ${successCount} 项配置`);
  }
}

const modifiedFields = computed(() =>
  Object.values(fieldsMap)
    .flat()
    .filter((f) => f.modified && f.id)
);
const modifiedCount = computed(() => modifiedFields.value.length);
const saveAllLoading = ref(false);

async function saveAll() {
  const modified = modifiedFields.value;
  if (modified.length === 0) return;
  saveAllLoading.value = true;
  let successCount = 0;
  for (const field of modified) {
    try {
      await ParamsAPI.updateParams(
        field.id!,
        {
          config_value: field.localValue,
          config_name: field.configName,
          config_key: field.configKey,
        },
        { showSuccessMessage: false }
      );
      field.modified = false;
      field.displayValue = field.localValue;
      successCount++;
    } catch {
      // 已由全局拦截器提示
    }
  }
  saveAllLoading.value = false;
  if (successCount > 0) {
    ElMessage.success(`已保存 ${successCount} 项配置`);
    configStore.isConfigLoaded = false;
    await configStore.getConfig();
  }
}

// ─── 初始化 ───

onMounted(async () => {
  if (!configStore.isConfigLoaded) {
    await configStore.getConfig();
  }
  rebuildFields();
});
</script>

<style scoped>
.param-save-bar {
  position: sticky;
  bottom: 0;
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: flex-end;
  padding: 12px 16px;
  margin-top: 12px;
  background: var(--fa-surface, var(--default-box-color));
  border-top: 1px solid var(--fa-border, var(--el-border-color-lighter));
}

.param-save-bar__text {
  font-size: var(--fa-font-sm, 12px);
  color: var(--el-text-color-secondary);
}

.params-side {
  width: 100%;
  height: 100%;
}

.params-nav-item {
  width: 100%;
  padding: 8px;
  font-size: 13px;
  color: var(--el-text-color-regular);
  text-align: left;
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: var(--fa-radius-sm, 8px);
}

.params-nav-item:hover {
  background: var(--el-fill-color-light);
}

.params-nav-item.is-active {
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}

.params-main {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 12px 16px;
}

.params-main__body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}
</style>
