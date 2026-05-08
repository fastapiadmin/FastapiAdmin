import type { App } from "vue";
import { createTerminal } from "vue-web-terminal";

/** vue-web-terminal：注册全局终端组件 */
export function initTerminal(app: App<Element>): void {
  app.use(createTerminal());
}
