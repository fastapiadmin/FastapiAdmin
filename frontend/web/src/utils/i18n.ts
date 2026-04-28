// translate router.meta.title, be used in breadcrumb sidebar tagsview
import i18n from '@/locales';
import type { Composer } from 'vue-i18n';

export function translateRouteTitle(title: any) {
  // 判断是否存在国际化配置，如果没有原生返回
  const hasKey = (i18n as Composer).global.te('route.' + title);
  if (hasKey) {
    const translatedTitle = (i18n as Composer).global.t('route.' + title);
    return translatedTitle;
  }
  return title;
}
