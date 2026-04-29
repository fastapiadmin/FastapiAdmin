<template>
  <div style="z-index: 999; border: 1px solid var(--el-border-color)">
    <!-- 工具栏 -->
    <Toolbar
      :editor="editorRef"
      mode="mode"
      :default-config="toolbarConfig"
      style="border-bottom: 1px solid var(--el-border-color)"
    />
    <!-- 编辑器 -->
    <Editor
      v-model="modelValue"
      :style="{ minHeight: height, overflowY: 'hidden' }"
      :default-config="editorConfig"
      mode="mode"
      @on-created="handleCreated"
      @on-change="handleChange"
    />
  </div>
</template>

<script setup lang="ts">
import "@wangeditor-next/editor/dist/css/style.css";
import { Toolbar, Editor } from "@wangeditor-next/editor-for-vue";
import { IToolbarConfig, IEditorConfig } from "@wangeditor-next/editor";
import ResourceAPI from "@/api/module_monitor/resource";

// 上传图片回调函数类型
type InsertFnType = (_url: string, _alt: string, _href: string) => void;

const props = defineProps({
  height: {
    type: String,
    default: "200px",
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  autoFocus: {
    type: Boolean,
    default: true,
  },
  scroll: {
    type: Boolean,
    default: true,
  },
});
// 双向绑定
const modelValue = defineModel("modelValue", {
  type: String,
  required: false,
});

// 编辑器实例，必须用 shallowRef，重要！
const editorRef = shallowRef();

// 工具栏配置
const toolbarConfig = ref<Partial<IToolbarConfig>>({});

// 编辑器配置 - 根据 props 动态生成配置
const editorConfig = ref<Partial<IEditorConfig>>({
  placeholder: "请输入内容...",
  readOnly: props.readonly,
  autoFocus: props.autoFocus,
  scroll: props.scroll,
  MENU_CONF: {
    uploadImage: {
      async customUpload(file: File, insertFn: InsertFnType) {
        const formData = new FormData();
        formData.append("file", file);

        try {
          const res = await ResourceAPI.uploadFile(formData);
          const data = res.data.data;

          insertFn(data.file_url, data.filename, data.file_url);
        } catch (error: any) {
          console.error("图片上传失败:", error);
          ElMessage.error("图片上传失败");
        }
      },
    } as any,
  },
});

// 记录 editor 实例，重要！
const handleCreated = (editor: any) => {
  editorRef.value = editor;
};

// 处理内容变化 - 获取纯文本而不是HTML
const handleChange = (editor: any) => {
  editorRef.value = editor;
  if (editorRef.value) {
    const text = editorRef.value.getText();
    modelValue.value = text;
  }
};

// 组件销毁时，也及时销毁编辑器，重要！
onBeforeUnmount(() => {
  const editor = editorRef.value;
  if (editor == null) return;
  editor.destroy();
});
</script>
