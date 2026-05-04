<template>
  <div>
    <!-- drawer -->
    <template v-if="modalConfig.component === 'drawer'">
      <el-drawer
        v-model="modalVisible"
        v-bind="{ destroyOnClose: true, ...modalConfig.drawer }"
        @close="handleClose"
      >
        <el-form ref="formRef" v-bind="modalConfig.form" :model="formData" :rules="formRules">
          <el-row :gutter="20">
            <template v-for="item in formItems" :key="item.prop">
              <el-col v-show="!item.hidden" v-bind="item.col">
                <el-form-item :label="item.label" :prop="item.prop">
                  <template #label>
                    <span>
                      {{ item?.label || "" }}
                      <el-tooltip v-if="item?.tips" v-bind="getTooltipProps(item.tips)">
                        <QuestionFilled class="mx-1 h-4 w-4" />
                      </el-tooltip>
                      <span v-if="modalConfig.colon" class="ml-0.5">:</span>
                    </span>
                  </template>

                  <template v-if="item.type === 'custom'">
                    <slot
                      :name="item.slotName ?? item.prop"
                      :prop="item.prop"
                      :form-data="formData"
                      :attrs="item.attrs"
                    />
                  </template>
                  <component
                    :is="componentMap.get(item.type)"
                    v-else
                    v-model.trim="formData[item.prop]"
                    v-bind="{ style: { width: '100%' }, ...item.attrs }"
                  >
                    <template v-if="['select', 'radio', 'checkbox'].includes(item.type)">
                      <component
                        :is="childrenMap.get(item.type)"
                        v-for="opt in item.options"
                        :key="opt.value"
                        :label="opt.label"
                        :value="opt.value"
                      />
                    </template>

                    <template v-if="item?.slotName && $slots[item.slotName]" #[item.slotName]>
                      <slot :name="item.slotName" />
                    </template>
                  </component>
                </el-form-item>
              </el-col>
            </template>
          </el-row>
        </el-form>

        <template #footer>
          <el-button v-if="!formDisable" type="primary" @click="handleSubmit">确 定</el-button>
          <el-button @click="handleClose">{{ !formDisable ? "取 消" : "关闭" }}</el-button>
        </template>
      </el-drawer>
    </template>
    <!-- dialog -->
    <template v-else>
      <EnhancedDialog
        v-model="modalVisible"
        :title="String(modalConfig.dialog?.title ?? '')"
        :width="modalConfig.dialog?.width ?? '600px'"
        :draggable="modalConfig.dialog?.draggable !== false"
        v-bind="dialogRestAttrs"
        @close="handleClose"
      >
        <el-form ref="formRef" v-bind="modalConfig.form" :model="formData" :rules="formRules">
          <el-scrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
            <el-row :gutter="20">
              <template v-for="item in formItems" :key="item.prop">
                <el-col v-show="!item.hidden" v-bind="item.col">
                  <el-form-item :label="item.label" :prop="item.prop">
                    <template #label>
                      <span>
                        {{ item?.label || "" }}
                        <el-tooltip v-if="item?.tips" v-bind="getTooltipProps(item.tips)">
                          <QuestionFilled class="mx-1 h-4 w-4" />
                        </el-tooltip>
                        <span v-if="modalConfig.colon" class="ml-0.5">:</span>
                      </span>
                    </template>

                    <template v-if="item.type === 'custom'">
                      <slot
                        :name="item.slotName ?? item.prop"
                        :prop="item.prop"
                        :form-data="formData"
                        :attrs="item.attrs"
                      />
                    </template>
                    <component
                      :is="componentMap.get(item.type)"
                      v-else
                      v-model.trim="formData[item.prop]"
                      v-bind="{ style: { width: '100%' }, ...item.attrs }"
                    >
                      <template v-if="['select', 'radio', 'checkbox'].includes(item.type)">
                        <component
                          :is="childrenMap.get(item.type)"
                          v-for="opt in item.options"
                          :key="opt.value"
                          :label="opt.label"
                          :value="opt.value"
                        />
                      </template>

                      <template v-if="item?.slotName && $slots[item.slotName]" #[item.slotName]>
                        <slot :name="item.slotName" />
                      </template>
                    </component>
                  </el-form-item>
                </el-col>
              </template>
            </el-row>
            <slot name="bottom" :form-data="formData" />
          </el-scrollbar>
        </el-form>

        <template #footer>
          <el-button v-if="!formDisable" type="primary" @click="handleSubmit">确 定</el-button>
          <el-button @click="handleClose">{{ !formDisable ? "取 消" : "关闭" }}</el-button>
        </template>
      </EnhancedDialog>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useThrottleFn } from "@vueuse/core";
import type { FormInstance, FormRules } from "element-plus";
import type { IModalConfig, IObject } from "./types";
import EnhancedDialog from "@/components/Core/overlays/EnhancedDialog.vue";
import { childrenMap, getTooltipProps, modalComponentMap as componentMap } from "./crudHelpers";

defineSlots<{ [key: string]: (_args: any) => any }>();

const props = defineProps<{ modalConfig: IModalConfig }>();
const emit = defineEmits<{ submitClick: []; customSubmit: [queryParams: IObject] }>();

const pk = props.modalConfig.pk ?? "id";

const dialogRestAttrs = computed(() => {
  const d = props.modalConfig.dialog ?? {};
  return { destroyOnClose: true, ...d };
});
const modalVisible = ref(false);
const formRef = ref<FormInstance>();
const formItems = reactive(props.modalConfig.formItems ?? []);
const formData = reactive<IObject>({});
const formRules: FormRules = {};
const formDisable = ref(false);

const handleClose = () => {
  modalVisible.value = false;
  formRef.value?.resetFields();
};

const setFormData = (data: IObject) => {
  for (const key in formData) {
    if (Object.prototype.hasOwnProperty.call(formData, key) && key in data) {
      formData[key] = data[key];
    }
  }
  if (Object.prototype.hasOwnProperty.call(data, pk)) {
    formData[pk] = data[pk];
  }
};

const handleSubmit = useThrottleFn(() => {
  formRef.value?.validate((valid: boolean) => {
    if (!valid) return;
    if (typeof props.modalConfig.beforeSubmit === "function") {
      props.modalConfig.beforeSubmit(formData);
    }
    if (!props.modalConfig?.formAction) {
      emit("customSubmit", formData);
      handleClose();
      return;
    }
    props.modalConfig.formAction(formData).then(() => {
      if (props.modalConfig.component === "drawer") {
        ElMessage.success(`${props.modalConfig.drawer?.title}成功`);
      } else {
        ElMessage.success(`${props.modalConfig.dialog?.title}成功`);
      }
      emit("submitClick");
      handleClose();
    });
  });
}, 3000);

onMounted(() => {
  formItems.forEach((item) => {
    if (item.initFn) {
      item.initFn(item);
    }
    formRules[item.prop] = item?.rules ?? [];
    props.modalConfig.form = { labelWidth: "auto", ...props.modalConfig?.form };

    if (["input-tag", "custom-tag", "cascader"].includes(item.type)) {
      formData[item.prop] = Array.isArray(item.initialValue) ? item.initialValue : [];
    } else if (item.type === "input-number") {
      formData[item.prop] = item.initialValue ?? null;
    } else {
      formData[item.prop] = item.initialValue ?? "";
    }
  });
});

defineExpose({
  setFormData,
  setModalVisible: (visible: boolean = true) => (modalVisible.value = visible),
  getFormData: (key: string) => formData[key] ?? formData,
  setFormItemData: (key: string, value: any) => (formData[key] = value),
  handleDisabled: (disable: boolean) => {
    formDisable.value = disable;
    props.modalConfig.form = {
      ...props.modalConfig.form,
      disabled: disable,
    };
  },
});
</script>

<style lang="scss" scoped>
:deep(.el-input-number .el-input__inner) {
  text-align: left;
}

:deep(.el-input-number.is-without-controls .el-input__wrapper) {
  padding-right: 11px !important ;
  padding-left: 11px !important;
}
</style>
