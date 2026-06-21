<!-- 租户切换器（顶栏版）：头像左侧，始终可见 -->
<template>
  <ElDropdown
    v-if="tenantList.length > 1"
    trigger="click"
    @command="handleSwitch"
    placement="bottom"
  >
    <span class="tenant-btn">
      <span class="tenant-icon">🏢</span>
      <span class="tenant-name">{{ currentTenantName }}</span>
      <FaSvgIcon icon="ri:arrow-down-s-line" class="arrow" />
    </span>
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem
          v-for="t in tenantList"
          :key="t.id"
          :command="t.id"
          :class="{ 'is-active': t.id === currentTenant?.id }"
        >
          <span class="dropdown-row">
            <span>{{ t.name }}</span>
            <FaSvgIcon v-if="t.id === currentTenant?.id" icon="ri:check-line" class="check" />
          </span>
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useUserStore } from "@stores";
import { storeToRefs } from "pinia";

defineOptions({ name: "FaTenantSwitcher" });

const userStore = useUserStore();
const { tenantList, currentTenant } = storeToRefs(userStore);

const currentTenantName = computed(
  () => currentTenant.value?.name || tenantList.value[0]?.name || "—"
);

async function handleSwitch(tenantId: number) {
  if (tenantId === currentTenant.value?.id) return;
  try {
    await userStore.selectTenant(tenantId);
    setTimeout(() => window.location.reload(), 200);
  } catch {
    // 静默失败
  }
}
</script>

<style scoped>
.tenant-btn {
  display: inline-flex;
  gap: 4px;
  align-items: center;
  max-width: 160px;
  height: 30px;
  padding: 0 10px 0 6px;
  font-size: 13px;
  color: var(--el-text-color-primary);
  cursor: pointer;
  user-select: none;
  background: var(--fa-gray-100);
  border: 1px solid var(--fa-gray-300);
  border-radius: 6px;
  transition:
    background 0.15s,
    border-color 0.15s;
}

.tenant-btn:hover {
  background: var(--fa-gray-200);
  border-color: var(--el-color-primary-light-5);
}

.tenant-icon {
  flex-shrink: 0;
  font-size: 15px;
  line-height: 1;
}

.tenant-name {
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
  white-space: nowrap;
}

.arrow {
  flex-shrink: 0;
  font-size: 11px;
  color: var(--el-text-color-secondary);
}

.dropdown-row {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.check {
  flex-shrink: 0;
  color: var(--el-color-primary);
}
</style>
