import type { ToastOptions } from 'wot-design-uni/components/wd-toast/types'

import { defineStore } from 'pinia'

interface GlobalLoading {
  loadingOptions: ToastOptions
  currentPage: string
}

const defaultOptions: ToastOptions = {
  show: false,
}
export const useGlobalLoading = defineStore('global-loading', {
  state: (): GlobalLoading => ({
    loadingOptions: defaultOptions,
    currentPage: '',
  }),
  getters: {},
  actions: {
    // 加载提示
    loading(option: ToastOptions | string) {
      this.currentPage = getCurrentPath()
      this.loadingOptions = CommonUtil.deepMerge({
        iconName: 'loading',
        duration: 0,
        cover: true,
        position: 'middle',
        show: true,
      }, typeof option === 'string' ? { msg: option } : option) as ToastOptions
    },
    // 关闭Toast
    close() {
      this.loadingOptions = defaultOptions
      this.currentPage = ''
    },
  },
})
