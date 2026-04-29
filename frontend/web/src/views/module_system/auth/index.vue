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
          Enterprise Ready
        </div>
        <h1 class="auth-feature__title">企业级管理系统</h1>
        <p class="auth-feature__subtitle">
          提供安全、高效、可扩展的管理解决方案，助力企业数字化转型与业务增长。
        </p>
        <ul class="auth-feature__highlights">
          <li>
            <span>✓</span>
            统一身份认证与权限管理
          </li>
          <li>
            <span>✓</span>
            支持定时任务与任务调度
          </li>
          <li>
            <span>✓</span>
            数据安全与操作审计
          </li>
          <li>
            <span>✓</span>
            灵活扩展与高可用架构
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
                {{ configStore.configData?.sys_web_title?.config_value || "" }}
              </span>
              <el-tooltip
                :content="configStore.configData?.sys_web_description?.config_value || ''"
                placement="bottom"
              >
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

        <!-- 登录页底部版权 -->
        <footer class="auth-panel__footer">
          <el-text size="small">
            <a :href="configStore.configData?.sys_git_code?.config_value || ''" target="_blank">
              {{ configStore.configData?.sys_web_copyright?.config_value || "" }}
            </a>
            |
            <a :href="configStore.configData?.sys_help_doc?.config_value || ''" target="_blank">
              帮助
            </a>
            |
            <a :href="configStore.configData?.sys_web_privacy?.config_value || ''" target="_blank">
              隐私
            </a>
            |
            <a :href="configStore.configData?.sys_web_clause?.config_value || ''" target="_blank">
              条款
            </a>
            {{ configStore.configData?.sys_keep_record?.config_value || "" }}
          </el-text>
        </footer>
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

let notificationInstance: ReturnType<typeof ElNotification> | null = null;

const showVoteNotification = () => {
  notificationInstance = ElNotification({
    title: "⭐ FastapiAdmin 完全开源 · 期待您的 Star 支持 🙏",
    message: `项目持续迭代中，若对您有所帮助，欢迎点亮 Star 支持！
    <br/><a href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank" style="color: var(--el-color-primary); text-decoration: none; font-weight: 500;">Github仓库 →</a>
    <br/><a href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank" style="color: var(--el-color-warning); text-decoration: none; font-weight: 500;">Gitee仓库 →</a>`,
    type: "success",
    position: "bottom-left",
    duration: 0,
    dangerouslyUseHTMLString: true,
  });
};

onMounted(() => {
  setTimeout(showVoteNotification, 500);
});

onBeforeUnmount(() => {
  if (notificationInstance) {
    notificationInstance.close();
    notificationInstance = null;
  }
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

.auth-panel__footer {
  padding-top: 0.875rem;
  margin-top: 0.125rem;
  font-size: 0.875rem;
  text-align: center;
  border-top: 1px solid var(--el-border-color-lighter);

  a {
    margin-left: 0.1rem;
    color: var(--el-text-color-regular);
    text-decoration: none;
    transition: color 0.2s ease;

    &:hover {
      color: var(--el-color-primary);
    }
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
