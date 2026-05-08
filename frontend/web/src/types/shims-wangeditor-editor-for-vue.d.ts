declare module "@wangeditor/editor-for-vue" {
  import type { DefineComponent } from "vue";

  export const Editor: DefineComponent<Record<string, unknown>, any, any>;
  export const Toolbar: DefineComponent<Record<string, unknown>, any, any>;
}
