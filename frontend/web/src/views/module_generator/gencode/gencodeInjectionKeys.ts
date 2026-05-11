import type { InjectionKey, Ref } from "vue";
import type { FormInstance } from "element-plus";
import type { CmComponentRef } from "codemirror-editor-vue3";

/** 代码生成抽屉内 el-form 与父页 ref 同步（校验/重置） */
export const GENCODE_BASIC_FORM_KEY: InjectionKey<Ref<FormInstance | undefined>> =
  Symbol("gencodeBasicForm");

/** 预览区 CodeMirror 与父页 ref 同步（主题） */
export const GENCODE_CM_KEY: InjectionKey<Ref<CmComponentRef | undefined>> = Symbol("gencodeCm");
