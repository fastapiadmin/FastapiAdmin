/*
 * @Author: weisheng
 * @Date: 2025-06-23 22:23:05
 * @LastEditTime: 2025-06-24 19:03:21
 * @LastEditors: weisheng
 * @Description:
 * @FilePath: /wot-starter/src/store/persist.ts
 * 记得注释
 */
import type { PiniaPluginContext } from 'pinia'

function persist({ store }: PiniaPluginContext, excludedIds: string[]) {
  // 检查当前store的id是否在排除列表中
  const isExcluded = excludedIds.includes(store.$id)

  // 如果当前store的id在排除列表中，则不进行持久化
  if (isExcluded) {
    return
  }

  // 暂存State
  let persistState = CommonUtil.deepClone(store.$state)
  // 从缓存中读取
  const storageState = uni.getStorageSync(store.$id)
  if (storageState) {
    persistState = storageState
  }
  store.$state = persistState
  store.$subscribe(() => {
    // 在存储变化的时候将store缓存
    uni.setStorageSync(store.$id, CommonUtil.deepClone(store.$state))
  })
}

export function persistPlugin(context: PiniaPluginContext) {
  // 调用persist函数，并传入排除列表
  persist(context, ['temp'])
}
