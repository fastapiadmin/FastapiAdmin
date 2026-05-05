/**
 * 锁屏状态管理模块
 *
 * 提供锁屏功能的状态管理
 *
 * ## 主要功能
 *
 * - 锁屏状态管理
 * - 锁屏密码验证
 * - 锁屏信息存储
 * - 解锁功能
 *
 * ## 使用场景
 *
 * - 用户离开时锁定屏幕
 * - 保护敏感操作
 * - 临时离开保护
 *
 * ## 持久化
 *
 * - 使用 localStorage 存储
 * - 锁屏状态跨页面保持
 *
 * @module store/modules/lock.store
 * @author FastapiAdmin Team
 */
import { defineStore } from "pinia";
import { ref } from "vue";

export const useLockStore = defineStore(
  "lockStore",
  () => {
    // 是否锁定屏幕
    const isLock = ref(false);
    // 锁屏密码
    const password = ref("");

    /**
     * 获取锁屏信息
     */
    const getLockInfo = () => ({
      isLock: isLock.value,
      password: password.value,
    });

    /**
     * 设置锁屏信息
     * @param lockInfo 锁屏信息对象
     */
    const setLockInfo = (lockInfo: { isLock?: boolean; password?: string }) => {
      if (lockInfo.isLock !== undefined) {
        isLock.value = lockInfo.isLock;
      }
      if (lockInfo.password !== undefined) {
        password.value = lockInfo.password;
      }
    };

    /**
     * 重置锁屏信息
     */
    const resetLockInfo = () => {
      isLock.value = false;
      password.value = "";
    };

    /**
     * 解锁屏幕
     * @param inputPassword 输入的解锁密码
     * @returns 是否解锁成功
     */
    const unLock = (inputPassword: string) => {
      if (password.value === inputPassword) {
        resetLockInfo();
        return true;
      } else {
        return false;
      }
    };

    return {
      isLock,
      password,
      getLockInfo,
      setLockInfo,
      resetLockInfo,
      unLock,
    };
  },
  {
    persist: true,
  }
);
