<template>
  <ElForm ref="formRef" class="gen-basic-step" :model="info" :rules="rules" label-width="120px">
    <!-- 顶部：生成回显 -->
    <ElRow :gutter="12" class="mb-3">
      <ElCol :span="24">
        <ElCard shadow="never" class="gen-echo-card">
          <div class="gen-echo-card__title">生成回显 / 生成文件路径</div>
          <div class="gen-echo-grid">
            <div class="gen-echo-item">
              <div class="gen-echo-item__k">后端路径</div>
              <code class="gen-echo-item__v">{{ backendModuleDirPreview }}</code>
            </div>
            <div class="gen-echo-item">
              <div class="gen-echo-item__k">前端视图路径</div>
              <code class="gen-echo-item__v">{{ frontendViewDirPreview }}</code>
            </div>
            <div class="gen-echo-item">
              <div class="gen-echo-item__k">前端 API 文件</div>
              <code class="gen-echo-item__v">{{ frontendApiFilePreview }}</code>
            </div>
            <div class="gen-echo-item">
              <div class="gen-echo-item__k gen-echo-item__k--with-tip">
                权限
                <ElTooltip
                  content="前两段为包名、模块名；第三段为操作类型（与接口/按钮一致）：query、detail、create、update、delete、patch、export、import、download。"
                  placement="top"
                >
                  <ElIcon class="gen-echo-item__tip"><QuestionFilled /></ElIcon>
                </ElTooltip>
              </div>
              <code class="gen-echo-item__v">{{ permissionPreview }}</code>
            </div>
          </div>
          <div
            v-if="info.sub_table_name && info.sub_table_fk_name && !info.master_sub_hint"
            class="gen-echo-warn"
          >
            将额外生成子表代码（不创建子表菜单）
          </div>
        </ElCard>
      </ElCol>
    </ElRow>

    <ElRow :gutter="16" class="gen-layout-row">
      <ElCol :span="24" class="gen-layout-left">
        <ElCard shadow="never" class="gen-form-card">
          <template #header>
            <div class="gen-form-card__header">
              <span class="font-medium">基础信息</span>
              <span class="gen-form-card__hint">切换步骤会先保存当前页</span>
            </div>
          </template>
          <ElRow :gutter="16">
            <ElCol :span="12">
              <ElFormItem label="表名称" prop="table_name">
                <ElInput v-model="info.table_name" placeholder="请输入表名称" />
              </ElFormItem>
            </ElCol>
            <ElCol :span="12">
              <ElFormItem label="表描述" prop="table_comment">
                <ElInput v-model="info.table_comment" placeholder="请输入表描述" />
              </ElFormItem>
            </ElCol>
            <ElCol :span="12">
              <ElFormItem label="实体类名称" prop="class_name">
                <ElInput v-model="info.class_name" placeholder="请输入" />
              </ElFormItem>
            </ElCol>
            <ElCol :span="12">
              <ElFormItem prop="package_name">
                <template #label>
                  包名
                  <ElTooltip
                    content="插件包名（plugin 顶层目录）。三段式示例：module_example"
                    placement="top"
                  >
                    <ElIcon><QuestionFilled /></ElIcon>
                  </ElTooltip>
                </template>
                <div class="gen-package-row">
                  <ElInput
                    v-model="info.package_name"
                    class="gen-package-row__input"
                    placeholder="例如 module_example"
                    clearable
                  />
                </div>
              </ElFormItem>
            </ElCol>
            <ElCol :span="12">
              <ElFormItem prop="module_name">
                <template #label>
                  模块名
                  <ElTooltip content="包名下第二层目录。示例：demo / gen_demo02" placement="top">
                    <ElIcon><QuestionFilled /></ElIcon>
                  </ElTooltip>
                </template>
                <ElInput v-model="info.module_name" placeholder="例如 demo" clearable />
              </ElFormItem>
            </ElCol>
            <ElCol :span="12">
              <ElFormItem prop="business_name">
                <template #label>
                  业务名
                  <ElTooltip
                    content="模块下第三层目录（可为空）。示例：demo01；留空表示仅到模块目录"
                    placement="top"
                  >
                    <ElIcon><QuestionFilled /></ElIcon>
                  </ElTooltip>
                </template>
                <ElInput
                  v-model="info.business_name"
                  placeholder="例如 demo01（可留空）"
                  clearable
                />
              </ElFormItem>
            </ElCol>
            <ElCol :span="12">
              <ElFormItem prop="function_name">
                <template #label>
                  功能名
                  <ElTooltip content="写入本地时作为菜单名称，例如 用户管理" placement="top">
                    <ElIcon><QuestionFilled /></ElIcon>
                  </ElTooltip>
                </template>
                <ElInput v-model="info.function_name" placeholder="例如 用户管理" />
              </ElFormItem>
            </ElCol>
            <ElCol :span="12">
              <ElFormItem>
                <template #label>
                  上级菜单
                  <ElTooltip content="仅可选目录；留空则在侧栏根下创建模块目录" placement="top">
                    <ElIcon><QuestionFilled /></ElIcon>
                  </ElTooltip>
                </template>
                <ElTreeSelect
                  v-model="info.parent_menu_id"
                  :data="menuOptions"
                  placeholder="不选=根目录下挂模块目录；选=挂到该目录下"
                  check-strictly
                  filterable
                  default-expand-all
                  :render-after-expand="false"
                  clearable
                  style="width: 100%"
                />
              </ElFormItem>
            </ElCol>
            <ElCol :span="24">
              <ElFormItem label="备注" prop="description">
                <ElInput v-model="info.description" type="textarea" :rows="3"></ElInput>
              </ElFormItem>
            </ElCol>
            <ElCol :span="24">
              <ElCard shadow="never" class="master-sub-card mb-4">
                <ElRow :gutter="16">
                  <ElCol :span="12">
                    <ElFormItem prop="sub_table_name">
                      <template #label>
                        子表表名
                        <ElTooltip
                          content="数据库中已存在的物理表名，例如 gen_order_item"
                          placement="top"
                        >
                          <ElIcon><QuestionFilled /></ElIcon>
                        </ElTooltip>
                      </template>
                      <ElInput
                        v-model="info.sub_table_name"
                        placeholder="与下栏同时填写，如 gen_order_item"
                        clearable
                        @blur="emit('master-sub-blur')"
                      />
                    </ElFormItem>
                  </ElCol>
                  <ElCol :span="12">
                    <ElFormItem prop="sub_table_fk_name">
                      <template #label>
                        子表外键列
                        <ElTooltip
                          content="子表中指向主表主键的列名，例如 order_id（类型需与主键匹配）"
                          placement="top"
                        >
                          <ElIcon><QuestionFilled /></ElIcon>
                        </ElTooltip>
                      </template>
                      <ElInput
                        v-model="info.sub_table_fk_name"
                        placeholder="与上栏同时填写，如 order_id"
                        clearable
                        @blur="emit('master-sub-blur')"
                      />
                    </ElFormItem>
                  </ElCol>
                </ElRow>
                <ElAlert
                  v-if="info.master_sub_hint"
                  class="mt-1"
                  type="warning"
                  :closable="false"
                  show-icon
                  :title="info.master_sub_hint"
                />
                <ElAlert
                  v-else-if="info.sub && info.sub_table_name && info.sub_table_fk_name"
                  class="mt-1"
                  type="success"
                  :closable="false"
                  show-icon
                  title="主子表结构已从数据库加载，预览与生成将包含子表代码。"
                />
              </ElCard>
            </ElCol>
          </ElRow>
        </ElCard>
      </ElCol>
    </ElRow>
  </ElForm>
</template>

<script setup lang="ts">
import { computed, inject, onUnmounted, ref, watch } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { QuestionFilled } from "@element-plus/icons-vue";
import type { GenTableSchema } from "@/api/module_generator/gencode";
import { GENCODE_BASIC_FORM_KEY } from "../gencodeInjectionKeys";

defineOptions({ name: "GenBasicStep" });

const props = defineProps<{
  info: GenTableSchema;
  rules: FormRules;
  menuOptions: OptionType[];
}>();

function findOptionByValue(options: OptionType[], value: number | string): any | null {
  for (const opt of options) {
    if (String(opt.value) === String(value)) return opt as any;
    if (opt.children?.length) {
      const hit = findOptionByValue(opt.children, value);
      if (hit) return hit;
    }
  }
  return null;
}

function inferPackageNameFromParentMenu(): string | null {
  const pid = props.info.parent_menu_id;
  if (pid == null) return null;
  const node = findOptionByValue(props.menuOptions || [], pid);
  const routePath = (node?.route_path ?? "").toString().trim();
  if (!routePath) return null;
  const seg = routePath.replace(/^\/+/, "").split("/", 1)[0]?.trim();
  if (!seg) return null;
  return seg.startsWith("module_") ? seg : `module_${seg}`;
}

const effectivePackageName = computed(() => {
  return inferPackageNameFromParentMenu() || (props.info.package_name || "").trim();
});

const permissionPreview = computed(() => {
  const pkg = effectivePackageName.value;
  const mod = (props.info.module_name || "").trim();
  if (!pkg || !mod) return "<module_xxx>:<module>:<操作>";
  // 与后端 permission_prefix + 模板一致；第三段为操作类型，示例用 query
  return `${pkg}:${mod}:query`;
});

const backendModuleDirPreview = computed(() => {
  const pkg = effectivePackageName.value;
  const mod = (props.info.module_name || "").trim();
  if (!pkg || !mod) return "backend/app/plugin/<module_xxx>/<module>/";
  return `backend/app/plugin/${pkg}/${mod}/`;
});

const frontendViewDirPreview = computed(() => {
  const pkg = effectivePackageName.value;
  const mod = (props.info.module_name || "").trim();
  if (!pkg || !mod) return "frontend/src/views/<module_xxx>/<module>/";
  return `frontend/src/views/${pkg}/${mod}/`;
});

const frontendApiFilePreview = computed(() => {
  const pkg = effectivePackageName.value;
  const mod = (props.info.module_name || "").trim();
  if (!pkg || !mod) return "frontend/src/api/<module_xxx>/<module>.ts";
  return `frontend/src/api/${pkg}/${mod}.ts`;
});

const emit = defineEmits<{
  "clear-master-sub": [];
  "master-sub-blur": [];
}>();

const formRef = ref<FormInstance>();
const injected = inject(GENCODE_BASIC_FORM_KEY, undefined);

/** 表名 → 合法目录片段（小写、下划线），用于无模块名时推导包名 */
function slugFromTableName(table: string): string {
  let s = table.trim().toLowerCase();
  if (!s) return "";
  if (s.startsWith("gen_")) s = s.slice(4);
  else if (s.startsWith("tb_")) s = s.slice(3);
  s = s
    .replace(/[^a-z0-9_]/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_|_$/g, "");
  return s || "table";
}

watch(
  () => [props.info.parent_menu_id, props.info.module_name, props.info.table_name] as const,
  () => {
    if (props.info.parent_menu_id != null) return;
    const current = (props.info.package_name || "").trim();
    if (current && current !== "gencode" && current !== "module_gencode") return;
    const mod = (props.info.module_name || "").trim();
    const tn = (props.info.table_name || "").trim();
    const slug = tn ? slugFromTableName(tn) : "";
    const next = mod
      ? mod.startsWith("module_")
        ? mod
        : `module_${mod}`
      : slug
        ? `module_${slug}`
        : "";
    if (next) props.info.package_name = next;
  },
  { immediate: true }
);

watch(
  formRef,
  (v) => {
    if (injected) injected.value = v;
  },
  { immediate: true }
);

onUnmounted(() => {
  if (injected) injected.value = undefined;
});
</script>

<style scoped lang="scss">
.gen-basic-step {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
}

.gen-basic-step ::deep(.el-col) {
  min-width: 0;
}

.gen-basic-step ::deep(.el-form-item__content) {
  min-width: 0;
}

.gen-basic-step ::deep(.el-input-group) {
  width: 100%;
  min-width: 0;
  max-width: 100%;
}

.gen-package-row {
  display: flex;
  gap: 8px;
  align-items: center;
  width: 100%;
  min-width: 0;
}

.gen-package-row__input {
  flex: 1;
  min-width: 0;
}

.master-sub-card {
  border: 1px solid var(--el-border-color-lighter);
}

.master-sub-card ::deep(.el-card__header) {
  padding: 8px 10px;
}

.master-sub-card ::deep(.el-card__body) {
  padding: 10px;
}

.gen-form-card {
  overflow-x: hidden;
  border: 1px solid var(--el-border-color-lighter);
}

.gen-form-card ::deep(.el-card__body) {
  overflow-x: hidden;
}

.gen-form-card__header {
  display: flex;
  gap: 12px;
  align-items: baseline;
  justify-content: space-between;
}

.gen-form-card__hint {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.gen-echo-card {
  border: 1px solid var(--el-border-color-lighter);
}

.gen-echo-card__title {
  padding: 6px 8px;
  font-size: 11px;
  font-weight: 600;
  background: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.gen-echo-card ::deep(.el-card__body) {
  padding: 6px 8px;
}

.gen-echo-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 12px;
  padding: 6px 8px;
}

.gen-echo-item {
  display: flex;
  gap: 10px;
  align-items: center;
  min-width: 0;
}

.gen-echo-item__k {
  flex: 0 0 auto;
  margin-bottom: 0;
  font-size: 11px;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.gen-echo-item__k--with-tip {
  display: inline-flex;
  gap: 4px;
  align-items: center;
}

.gen-echo-item__tip {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  cursor: help;
}

.gen-echo-item__v {
  display: block;
  flex: 1;
  min-width: 0;
  padding: 1px 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 11px;
  white-space: nowrap;
  background: var(--el-fill-color);
  border-radius: 3px;
}

.gen-echo-warn {
  padding: 0 8px 6px;
  font-size: 11px;
  color: var(--el-color-warning);
}
</style>
