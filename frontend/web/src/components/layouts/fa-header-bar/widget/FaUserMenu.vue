<!-- 用户菜单：合并旧版顶栏（配置中心、Gitee、引导）+ 新版 Popover 与链接结构 -->
<template>
  <!-- inline-flex + items-center：与顶栏 FaIconButton 同一中线对齐，避免 Popover 触发层基线偏移 -->
  <div class="fa-user-menu inline-flex shrink-0 items-center leading-none">
    <ElPopover
      ref="userMenuPopover"
      placement="bottom-end"
      :width="240"
      :hide-after="0"
      :offset="10"
      trigger="hover"
      :show-arrow="false"
      popper-class="user-menu-popover"
      popper-style="padding: 5px 16px;"
    >
      <template #reference>
        <div
          class="fa-user-menu__avatar-ref mr-5 max-sm:mr-[16px] c-p flex size-8.5 max-sm:w-6.5 max-sm:h-6.5 shrink-0 items-center justify-center"
        >
          <img
            v-if="userAvatar"
            class="size-full rounded-full object-cover block"
            :src="userAvatar"
            alt="avatar"
          />
          <img
            v-else
            class="size-full rounded-full block"
            src="@imgs/user/avatar.webp"
            alt="avatar"
          />
          <!-- 与旧版 NavbarActions.user-profile__online-indicator 一致 -->
          <span class="fa-user-menu__online-dot" aria-hidden="true" />
        </div>
      </template>
      <template #default>
        <div class="pt-3">
          <div class="flex-c pb-1 px-0">
            <img
              v-if="userAvatar"
              class="w-10 h-10 mr-3 ml-0 overflow-hidden rounded-full float-left object-cover"
              :src="userAvatar"
              alt=""
            />
            <img
              v-else
              class="w-10 h-10 mr-3 ml-0 overflow-hidden rounded-full float-left"
              src="@imgs/user/avatar.webp"
              alt=""
            />
            <div class="w-[calc(100%-60px)] h-full">
              <span class="block text-sm font-medium text-g-800 truncate">
                {{ displayName }}
              </span>
              <span class="block mt-0.5 text-xs text-g-500 truncate">{{ displayEmail }}</span>
            </div>
          </div>
          <ul class="py-4 mt-3 border-t border-g-300/80">
            <li class="btn-item" @click="goPage('/profile')">
              <FaSvgIcon icon="ri:user-3-line" />
              <span>{{ $t("topBar.user.userCenter") }}</span>
            </li>
            <li class="btn-item" @click="goChangeLog">
              <FaSvgIcon icon="ri:draft-line" />
              <span>{{ $t("topBar.user.changeLog") }}</span>
            </li>
            <li class="btn-item" @click="openParamConfig">
              <FaSvgIcon icon="ri:settings-3-line" />
              <span>{{ $t("topBar.user.paramConfig") }}</span>
            </li>
            <li class="btn-item" @click="toDocs()">
              <FaSvgIcon icon="ri:book-2-line" />
              <span>{{ $t("topBar.user.docs") }}</span>
            </li>
            <li class="btn-item" @click="toGithub()">
              <FaSvgIcon icon="ri:github-line" />
              <span>{{ $t("topBar.user.github") }}</span>
            </li>
            <li class="btn-item" @click="toGitee">
              <FaSvgIcon icon="ri:git-branch-line" />
              <span>{{ $t("topBar.user.gitee") }}</span>
            </li>
            <li class="btn-item" @click="startTour">
              <FaSvgIcon icon="ri:compass-3-line" />
              <span>{{ $t("topBar.user.tour") }}</span>
            </li>
            <li class="btn-item" @click="lockScreen()">
              <FaSvgIcon icon="ri:lock-line" />
              <span>{{ $t("topBar.user.lockScreen") }}</span>
            </li>
            <div class="w-full h-px my-2 bg-g-300/80"></div>
            <li class="btn-item btn-item--logout" @click="handleLogout">
              {{ $t("topBar.user.logout") }}
            </li>
          </ul>
        </div>
      </template>
    </ElPopover>

    <ConfigInfoDrawer v-model="paramDrawerVisible" />
  </div>
</template>

<script setup lang="ts">
import { watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { ElMessageBox } from "element-plus";
import ConfigInfoDrawer from "@views/module_system/param/components/ConfigInfoDrawer.vue";
import { useAppStore } from "@stores/modules/app.store";
import { useSettingsStore } from "@stores/modules/setting.store";
import { useUserStore } from "@stores/modules/user.store";
import { WEB_LINKS } from "@utils/constants";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { mittBus } from "@utils/sys";

defineOptions({ name: "FaUserMenu" });

const router = useRouter();
const { t } = useI18n();
const userStore = useUserStore();
const appStore = useAppStore();
const settingStore = useSettingsStore();

const { info: userInfo } = storeToRefs(userStore);
const userMenuPopover = ref();
const paramDrawerVisible = ref(false);

const userAvatar = computed(() => {
  const a = (userInfo.value as { avatar?: string })?.avatar?.trim();
  return a || "";
});

const displayName = computed(
  () =>
    (userInfo.value as { name?: string; username?: string })?.name ||
    (userInfo.value as { username?: string })?.username ||
    "—"
);

const displayEmail = computed(() => (userInfo.value as { email?: string })?.email || "");

/** 与旧版 NavbarActions 一致：桌面浮动引导，移动端进引导页 */
const guideVisible = computed({
  get: () => appStore.guideVisible,
  set: (v: boolean) => appStore.showGuide(v),
});

function openParamConfig(): void {
  closeUserMenu();
  paramDrawerVisible.value = true;
}

function goPage(path: string): void {
  router.push(path);
}

function goChangeLog(): void {
  closeUserMenu();
  router.push({ name: "ChangeLog" }).catch(() => {});
}

function toDocs(): void {
  window.open(WEB_LINKS.DOCS);
}

function toGithub(): void {
  window.open(WEB_LINKS.GITHUB);
}

function toGitee(): void {
  window.open(WEB_LINKS.GITEE);
}

function lockScreen(): void {
  mittBus.emit("openLockScreen");
}

function startTour(): void {
  closeUserMenu();
  if (appStore.device === DeviceEnum.MOBILE) {
    router.push({ name: "Guide" });
  } else {
    guideVisible.value = true;
  }
}

watch(
  () => guideVisible.value,
  (val, oldVal) => {
    if (oldVal && !val) {
      settingStore.updateSetting("showGuide", false);
    }
  }
);

function handleLogout(): void {
  closeUserMenu();
  setTimeout(() => {
    ElMessageBox.confirm(t("common.logoutTips"), t("common.tips"), {
      confirmButtonText: t("common.confirm"),
      cancelButtonText: t("common.cancel"),
      customClass: "login-out-dialog",
    }).then(() => {
      userStore.logout();
    });
  }, 200);
}

function closeUserMenu(): void {
  setTimeout(() => {
    userMenuPopover.value?.hide?.();
  }, 100);
}
</script>

<style scoped>
@reference '@styles/core/tailwind.css';

@layer components {
  .btn-item {
    @apply flex items-center p-2 mb-3 select-none rounded-md cursor-pointer last:mb-0;

    span {
      @apply text-sm;
    }

    .fa-svg-icon {
      @apply mr-2 text-base;
    }

    &:hover {
      background-color: var(--fa-gray-200);
    }
  }

  /** 退出：沿用菜单项 hover 底纹，并加重边框/文字，避免仅 shadow 几乎无反馈 */
  .btn-item.btn-item--logout {
    @apply justify-center mt-5 mb-0 py-1.5 text-xs border border-g-400;

    &:hover {
      color: var(--el-color-danger);
      background-color: var(--fa-gray-200);
      border-color: var(--el-color-danger-light-3);
    }
  }
}

/* ElPopover 基于 Tooltip：触发层默认 inline-block，与顶栏 flex 图标中线对齐 */
.fa-user-menu .el-tooltip__trigger {
  display: inline-flex !important;
  align-items: center;
  line-height: 1;
}

/* 顶栏头像右下角在线状态（对齐旧版顶栏）；占位与 FaIconButton size-8.5 一致 */
.fa-user-menu__avatar-ref {
  position: relative;
  box-sizing: border-box;
}

.fa-user-menu__online-dot {
  position: absolute;
  right: 0;
  bottom: 0;
  z-index: 1;
  width: 8px;
  height: 8px;
  pointer-events: none;
  background-color: var(--el-color-success);
  border-radius: 50%;
  box-shadow: 0 0 2px rgb(0 0 0 / 20%);
}
</style>
