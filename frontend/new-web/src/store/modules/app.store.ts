/**
 * 应用状态管理模块（兼容 web 项目）
 *
 * 提供应用相关的状态管理
 *
 * ## 主要功能
 *
 * - 设备类型管理（桌面/平板/移动端）
 * - 布局大小管理（默认/紧凑/宽松）
 * - 语言管理（中文/英文）
 * - 侧边栏状态管理（展开/收起）
 * - 顶部菜单激活路径管理
 * - 引导功能可见性管理
 *
 * ## 使用场景
 *
 * - 响应式布局适配
 * - 多语言切换
 * - 侧边栏折叠展开
 * - 顶部菜单导航
 * - 新手引导展示
 *
 * @module store/modules/app.store
 * @author FastapiAdmin Team
 */
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { DeviceEnum } from "@/enums/settings/device.enum";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import en from "element-plus/es/locale/lang/en";

export const useAppStore = defineStore(
  "appStore",
  () => {
    /** 设备类型 */
    const device = ref<string>(DeviceEnum.DESKTOP);

    /** 布局大小 */
    const size = ref<string>("default");

    /** 语言 */
    const language = ref<string>("zh");

    /** 侧边栏状态 */
    const sidebar = ref({
      opened: true,
      withoutAnimation: false,
    });

    /** 顶部菜单激活路径 */
    const activeTopMenuPath = ref<string>("");

    /** 引导可见性 */
    const guideVisible = ref<boolean>(false);

    /** 语言区域 */
    const locale = computed(() => {
      return language.value === "en" ? en : zhCn;
    });

    /** 切换侧边栏 */
    function toggleSidebar() {
      sidebar.value.opened = !sidebar.value.opened;
    }

    /** 关闭侧边栏 */
    function closeSideBar() {
      sidebar.value.opened = false;
    }

    /** 打开侧边栏 */
    function openSideBar() {
      sidebar.value.opened = true;
    }

    /** 切换设备 */
    function toggleDevice(val: string) {
      device.value = val;
    }

    /** 改变布局大小 */
    function changeSize(val: string) {
      size.value = val;
    }

    /** 改变语言 */
    function changeLanguage(val: string) {
      language.value = val;
    }

    /** 顶部菜单切换 */
    function activeTopMenu(val: string) {
      activeTopMenuPath.value = val;
    }

    /** 显示或隐藏引导 */
    function showGuide(val: boolean) {
      guideVisible.value = val;
    }

    return {
      device,
      sidebar,
      language,
      locale,
      size,
      activeTopMenu,
      toggleDevice,
      showGuide,
      changeSize,
      changeLanguage,
      toggleSidebar,
      closeSideBar,
      openSideBar,
      activeTopMenuPath,
      guideVisible,
    };
  },
  {
    persist: true,
  }
);
