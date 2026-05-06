import type { App } from "vue";
import { InstallCodeMirror } from "codemirror-editor-vue3";

export function initCodeMirror(app: App<Element>): void {
  app.use(InstallCodeMirror);
}
