import type { App } from 'vue';
import i18n from '@/locales';

export function initI18n(app: App<Element>) {
  app.use(i18n);
}
