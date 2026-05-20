<template>
  <div class="auth-view" :style="{ '--login-background-url': `url(${loginBackgroundUrl})` }">
    <!-- 右侧切换主题、语言按钮  -->
    <div class="auth-view__toolbar">
      <el-tooltip :content="t('login.themeToggle')" placement="bottom">
        <CommonWrapper>
          <ThemeSwitch />
        </CommonWrapper>
      </el-tooltip>
      <el-tooltip :content="t('login.languageToggle')" placement="bottom">
        <CommonWrapper>
          <LangSelect size="text-20px" />
        </CommonWrapper>
      </el-tooltip>
    </div>
    <!-- 登录页主体 -->
    <div class="auth-view__wrapper">
      <!-- 可选：左侧产品介绍区域，如不需要可整段删除，右侧登录表单会自动居中展示 -->
      <section class="auth-feature">
        <div class="auth-feature__badge">
          <span class="auth-feature__dot" />
          招生联动平台
        </div>
        <h1 class="auth-feature__title">高中高校联动项目</h1>
        <p class="auth-feature__subtitle">
          面向高中与高校的招生咨询、宣传联动与数据协同，支撑多部门、多角色协同办公与信息共享。
        </p>
        <ul class="auth-feature__highlights">
          <li>
            <span>✓</span>
            招生咨询会与信息采集管理
          </li>
          <li>
            <span>✓</span>
            高校库与宣传联动业务协同
          </li>
          <li>
            <span>✓</span>
            统一权限与跨部门数据共享
          </li>
          <li>
            <span>✓</span>
            审核流程与操作留痕可追溯
          </li>
        </ul>
      </section>

      <!-- 登录页主体容器 -->
      <section class="auth-panel">
        <!-- 标题 -->
        <div class="auth-panel__brand">
          <div class="auth-panel__logo-wrap">
            <!-- logo -->
            <el-image
              :src="configStore.configData?.sys_web_logo?.config_value || ''"
              class="auth-panel__logo"
            />
          </div>
          <div class="auth-panel__meta">
            <div class="auth-panel__title-row">
              <span class="auth-panel__title">
                {{ webTitle }}
              </span>
              <el-tooltip :content="webDescription" placement="bottom">
                <el-icon class="cursor-help"><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="auth-panel__version-row">
              <span class="auth-panel__version-label">Version</span>
              <span class="auth-panel__version-pill">
                v{{ configStore.configData?.sys_web_version?.config_value || "" }}
              </span>
            </div>
          </div>
        </div>
        <!-- 组件切换 -->
        <transition name="fade-slide" mode="out-in">
          <component
            :is="formComponents[component]"
            v-model="component"
            v-model:preset-username="loginPreset.username"
            v-model:preset-password="loginPreset.password"
            class="auth-panel__form"
          />
        </transition>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
// import logo from "@/assets/logo.png";
// import { defaultSettings } from "@/settings";
import CommonWrapper from "@/components/CommonWrapper/index.vue";
import ThemeSwitch from "@/components/ThemeSwitch/index.vue";
import { useConfigStore } from "@/store";

const configStore = useConfigStore();

const DEFAULT_WEB_TITLE = "高中高校联动平台";
const DEFAULT_WEB_DESCRIPTION = "高中与高校招生咨询、宣传联动与数据协同管理平台";

/** 登录页标头：兼容库内仍为 FastApiAdmin 的旧配置 */
const webTitle = computed(() => {
  const value = configStore.configData?.sys_web_title?.config_value?.trim();
  if (!value || /^fastapiadmin$/i.test(value)) {
    return DEFAULT_WEB_TITLE;
  }
  return value;
});

const webDescription = computed(() => {
  const value = configStore.configData?.sys_web_description?.config_value?.trim();
  if (!value || /fastapiadmin|完全开源|权限管理系统/i.test(value)) {
    return DEFAULT_WEB_DESCRIPTION;
  }
  return value;
});

// 添加计算属性处理背景图片URL
const loginBackgroundUrl = computed(() => {
  // 使用可选链操作符确保安全访问
  return (
    configStore.configData?.sys_login_background?.config_value ||
    new URL("@/assets/images/login-bg.svg", import.meta.url).href
  );
});

type LayoutMap = "login" | "register" | "resetPwd";

const t = useI18n().t;

const component = ref<LayoutMap>("login"); // 切换显示的组件
const formComponents = {
  login: defineAsyncComponent(() => import("./components/Login.vue")),
  register: defineAsyncComponent(() => import("./components/Register.vue")),
  resetPwd: defineAsyncComponent(() => import("./components/ResetPwd.vue")),
};

// 预填登录信息（通过具名 v-model 双向绑定传递）
const loginPreset = reactive<{ username: string; password: string }>({
  username: "admin",
  password: "123456",
});

</script>

<style lang="scss" scoped>
.auth-view {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: clamp(1rem, 3vw, 2rem);
  overflow: hidden;
  background-color: var(--el-bg-color-page);

  &::before {
    position: fixed;
    inset: 0;
    z-index: -2;
    content: "";
    background: var(--login-background-url) center/cover no-repeat;
  }

  &::after {
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    content: "";
    background: linear-gradient(120deg, var(--el-bg-color), transparent);
  }
}

.auth-view__toolbar {
  display: inline-flex;
  gap: 0.75rem;
  align-self: flex-end;
  padding: 0.5rem 0.75rem;
  background-color: var(--el-bg-color-overlay);
  border: 1px solid var(--el-border-color-light);
  border-radius: 999px;
  box-shadow: var(--el-box-shadow-light);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;

  &:hover {
    box-shadow: var(--el-box-shadow);
    transform: translateY(-2px);
  }

  @media (max-width: 640px) {
    position: fixed;
    top: 12px;
    right: 16px;
    z-index: 20;
    align-self: flex-end;
    justify-content: center;
  }

  // 暗色/亮色交给 Element Plus 变量处理，不在页面里写死颜色分支
}

/* 暗色样式交给全局主题变量 */

.auth-view__wrapper {
  display: grid;
  flex: 1;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: clamp(1.5rem, 3vw, 3rem);
  align-items: stretch;
  padding: clamp(1.5rem, 2vw, 2.5rem);
}

.auth-feature {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(1.5rem, 3vw, 3rem);
  color: var(--el-text-color-primary);
  animation: featureFade 0.8s ease-out;
}

@media (max-width: 768px) {
  .auth-view__wrapper {
    display: block;
    padding: 1.25rem 0.75rem 1.75rem;
  }

  .auth-feature {
    display: none;
  }

  .auth-panel {
    width: 100%;
    margin-inline: 0;
    box-shadow: var(--el-box-shadow);
  }
}

.auth-feature__badge {
  display: inline-flex;
  gap: 0.5rem;
  align-items: center;
  width: fit-content;
  padding: 0.3rem 0.9rem;
  font-size: 0.875rem;
  color: var(--el-color-primary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: var(--el-color-primary-light-9);
  border-radius: 999px;
}

.auth-feature__dot {
  width: 0.5rem;
  height: 0.5rem;
  background: var(--el-color-primary);
  border-radius: 50%;
  box-shadow: var(--el-box-shadow-light);
}

.auth-feature__title {
  margin: 1.5rem 0 0.5rem;
  font-size: clamp(2rem, 4vw, 2.75rem);
  font-weight: 600;
  line-height: 1.2;
}

.auth-feature__subtitle {
  margin-bottom: 1.5rem;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--el-text-color-regular);
}

.auth-feature__highlights {
  display: grid;
  gap: 0.75rem;
  padding: 0;
  margin: 0;
  list-style: none;

  li {
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
    padding: 0.75rem 1rem;
    font-weight: 500;
    color: var(--el-text-color-primary);
    background: var(--el-bg-color-overlay);
    border: 1px solid var(--el-border-color-lighter);
    border-radius: 12px;
    backdrop-filter: blur(6px);

    span {
      font-size: 0.75rem;
      line-height: 1.6;
      color: var(--el-color-primary);
    }
  }
}

.auth-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  justify-content: flex-start;
  justify-self: end;
  width: min(520px, 100%);
  padding: clamp(2rem, 3vw, 2.75rem);
  margin-inline: auto;
  background: var(--el-bg-color-overlay);
  border: 1px solid var(--el-border-color-light);
  border-radius: 24px;
  box-shadow: var(--el-box-shadow);
  backdrop-filter: blur(20px);
  animation: panelLift 0.7s ease;
}

.auth-panel__brand {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 0.85rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.auth-panel__logo-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  background: var(--el-fill-color-light);
  border-radius: 18px;
  box-shadow: var(--el-box-shadow-light);
}

.auth-panel__logo {
  flex-shrink: 0;
  width: 52px;
  height: 52px;
}

.auth-panel__meta {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 0;
}

.auth-panel__title-row {
  display: flex;
  gap: 0.5rem;
  align-items: baseline;
}

.auth-panel__title {
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 1.2rem;
  font-weight: 650;
  line-height: 1.4;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.auth-panel__version-row {
  display: inline-flex;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.78rem;
}

.auth-panel__version-label {
  color: var(--el-text-color-placeholder);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.auth-panel__version-pill {
  padding: 0.1rem 0.55rem;
  font-weight: 500;
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 999px;
}

.auth-panel__form {
  width: 100%;
  max-width: 100%;
  margin-inline: auto;

  :deep(.el-form-item) {
    margin-bottom: 1.25rem;
  }

  :deep(.el-input__wrapper) {
    box-shadow: 0 0 0 1px var(--el-border-color) inset;
    transition: all 0.2s ease;

    &:hover {
      box-shadow: 0 0 0 1px var(--el-border-color-hover) inset;
    }

    &.is-focus {
      box-shadow: 0 0 0 1px var(--el-color-primary) inset;
    }
  }

  :deep(.el-card) {
    background: transparent;
    box-shadow: none;
  }
}

@keyframes featureFade {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes panelLift {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(-40px) scale(0.95);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(40px) scale(0.95);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
}
</style>
