import type { App } from 'vue';
import ElementPlus from 'element-plus';

export function initElementPlus(app: App<Element>) {
  app.use(ElementPlus);
}
