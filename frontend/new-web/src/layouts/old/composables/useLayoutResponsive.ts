import { watchEffect, computed } from "vue";
import { useWindowSize } from "@vueuse/core";
import { useAppStore } from "@/store";
import { DeviceEnum } from "@/enums/settings/device.enum";

/**
 * 设备检测和响应式处理
 * 监听屏幕尺寸变化，自动调整设备类型和侧边栏状态
 */
export function useLayoutResponsive() {
  const appStore = useAppStore();
  const { width } = useWindowSize();

  // 定义响应式断点
  const WIDTH_DESKTOP = 992; // 桌面设备断点 (>=992px)

  // 计算设备类型
  const isDesktop = computed(() => width.value >= WIDTH_DESKTOP);
  const isMobile = computed(() => appStore.device === DeviceEnum.MOBILE);

  // 设置当前设备类型并调整侧边栏状态
  watchEffect(() => {
    const deviceType = isDesktop.value ? DeviceEnum.DESKTOP : DeviceEnum.MOBILE;

    // 更新设备类型
    appStore.toggleDevice(deviceType);

    // 根据设备类型调整侧边栏状态
    if (isDesktop.value) {
      appStore.openSideBar();
    } else {
      appStore.closeSideBar();
    }
  });

  return {
    isDesktop,
    isMobile,
  };
}
