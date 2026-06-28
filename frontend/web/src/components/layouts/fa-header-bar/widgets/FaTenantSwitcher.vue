<!-- 顶栏租户切换器：头像左侧，始终可见 -->
<template>
  <ElDropdown
    v-if="tenantList.length > 1"
    trigger="click"
    placement="bottom-start"
    :disabled="switching"
    @command="handleSwitch"
    @visible-change="(v) => (dropdownVisible = v)"
    popper-class="fa-tenant-dropdown"
  >
    <div
      class="tenant-switcher"
      :class="{ 'is-active': dropdownVisible, 'is-switching': switching }"
      :title="`当前租户：${currentTenantName}`"
    >
      <FaSvgIcon icon="ri:building-2-fill" class="icon" />
      <span class="name">{{ currentTenantName }}</span>
      <FaSvgIcon
        v-if="!switching"
        icon="ri:arrow-down-s-line"
        class="arrow"
        :class="{ rotated: dropdownVisible }"
      />
      <ElIcon v-else class="arrow is-loading"><Loading /></ElIcon>
    </div>
    <template #dropdown>
      <ElDropdownMenu>
        <div class="dropdown-header">
          <span class="dropdown-title">切换租户</span>
          <ElTag size="small" effect="plain" type="info"> 共 {{ tenantList.length }} 个 </ElTag>
        </div>
        <ElDropdownItem
          v-for="t in tenantList"
          :key="t.id"
          :command="t.id"
          :class="{ 'is-active': t.id === currentTenant?.id }"
          :disabled="switching"
        >
          <div class="dropdown-item" :class="{ 'is-current': t.id === currentTenant?.id }">
            <div class="item-main">
              <FaSvgIcon
                :icon="t.id === currentTenant?.id ? 'ri:check-line' : 'ri:building-2-line'"
                class="item-icon"
                :class="{ active: t.id === currentTenant?.id }"
              />
              <div class="item-text">
                <div class="item-name">{{ t.name }}</div>
                <div v-if="t.code" class="item-code">{{ t.code }}</div>
              </div>
            </div>
            <ElTag v-if="t.id === currentTenant?.id" type="primary" size="small" effect="plain">
              当前
            </ElTag>
          </div>
        </ElDropdownItem>
        <div class="dropdown-footer-hint">
          <FaSvgIcon icon="ri:information-line" class="hint-icon" />
          <span>点击其他租户即可切换</span>
        </div>
        <div v-if="switching" class="dropdown-footer">
          <ElIcon class="is-loading"><Loading /></ElIcon>
          <span>切换中...</span>
        </div>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { ElMessage } from "element-plus";
import { Loading } from "@element-plus/icons-vue";
import { useUserStore } from "@stores";
import { storeToRefs } from "pinia";

defineOptions({ name: "FaTenantSwitcher" });

const userStore = useUserStore();
const { tenantList, currentTenant } = storeToRefs(userStore);

const dropdownVisible = ref(false);
const switching = ref(false);

const currentTenantName = computed(
  () => currentTenant.value?.name || tenantList.value[0]?.name || "—"
);

async function handleSwitch(tenantId: number) {
  if (switching.value) return;
  // 点击当前租户：给个明确提示（不再静默忽略）
  if (tenantId === currentTenant.value?.id) {
    ElMessage.info("已是当前租户");
    return;
  }
  switching.value = true;
  try {
    await userStore.selectTenant(tenantId);
    setTimeout(() => window.location.reload(), 200);
  } catch {
    switching.value = false;
  }
}
</script>

<style scoped>
.tenant-switcher {
  display: inline-flex;
  gap: 6px;
  align-items: center;
  max-width: 180px;
  height: 32px;
  padding: 0 10px;
  font-size: 13px;

  @media (width <= 640px) {
    max-width: 120px;
    padding: 0 8px;
    font-size: 12px;
  }

  color: var(--el-text-color-primary);
  cursor: pointer;
  user-select: none;
  background: var(--fa-gray-100);
  border: 1px solid var(--fa-gray-300);
  border-radius: 6px;
  transition: all 0.15s;

  &:hover {
    color: var(--el-color-primary);
    background: var(--el-color-primary-light-9);
    border-color: var(--el-color-primary-light-5);
  }

  &.is-active {
    color: var(--el-color-primary);
    background: var(--el-color-primary-light-9);
    border-color: var(--el-color-primary);
  }

  &.is-switching {
    cursor: wait;
    opacity: 0.7;
  }

  .icon {
    flex-shrink: 0;
    font-size: 14px;
  }

  .name {
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 500;
    white-space: nowrap;
  }

  .arrow {
    flex-shrink: 0;
    font-size: 12px;
    color: var(--el-text-color-secondary);
    transition: transform 0.2s;

    &.rotated {
      transform: rotate(180deg);
    }
  }
}
</style>

<style lang="scss">
/* 全局样式：下拉面板（scoped 无法深入 ElDropdownMenu） */
.fa-tenant-dropdown {
  min-width: 240px;
  max-width: calc(100vw - 20px);
  padding: 0 !important;

  @media (width <= 640px) {
    width: 90vw;
    min-width: 200px;
  }

  .el-dropdown-menu__item {
    padding: 0 !important;

    &.is-active {
      color: inherit;
      background: transparent !important;
    }

    &:not(.is-disabled):hover {
      background: var(--fa-gray-200) !important;
    }
  }

  .dropdown-header {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    border-bottom: 1px solid var(--el-border-color-lighter);
  }

  .dropdown-title {
    font-size: 12px;
    font-weight: 500;
    color: var(--el-text-color-secondary);
  }

  .dropdown-item {
    display: flex;
    gap: 12px;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 8px 12px;
    border-left: 2px solid transparent;
    border-radius: 0;
    transition: all 0.15s;

    &.is-current {
      background: var(--el-color-primary-light-9);
      border-left-color: var(--el-color-primary);

      &:hover {
        background: var(--el-color-primary-light-8);
      }
    }
  }

  .dropdown-footer-hint {
    display: flex;
    gap: 4px;
    align-items: center;
    justify-content: center;
    padding: 6px 12px 8px;
    font-size: 11px;
    color: var(--el-text-color-secondary);
    border-top: 1px solid var(--el-border-color-lighter);

    .hint-icon {
      font-size: 12px;
    }
  }

  .item-main {
    display: flex;
    flex: 1;
    gap: 8px;
    align-items: center;
    min-width: 0;
  }

  .item-icon {
    flex-shrink: 0;
    font-size: 15px;
    color: var(--el-text-color-secondary);

    &.active {
      color: var(--el-color-primary);
    }
  }

  .item-text {
    min-width: 0;
  }

  .item-name {
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 13px;
    font-weight: 500;
    color: var(--el-text-color-primary);
    white-space: nowrap;
  }

  .item-code {
    margin-top: 2px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 11px;
    color: var(--el-text-color-secondary);
    white-space: nowrap;
  }

  .dropdown-footer {
    display: flex;
    gap: 6px;
    align-items: center;
    justify-content: center;
    padding: 8px 12px;
    font-size: 12px;
    color: var(--el-text-color-secondary);
    border-top: 1px solid var(--el-border-color-lighter);
  }
}
</style>
