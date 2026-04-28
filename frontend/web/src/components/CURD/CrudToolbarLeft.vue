<!-- 列表页左侧工具栏：1) configButtons 与 PageContent 配置驱动一致 2) perm 预设「新增/批删/更多」 3) 默认插槽完全自定义 -->
<template>
  <div class="data-table__toolbar--left">
    <template v-if="configButtons && configButtons.length">
      <template v-for="(btn, index) in configButtons" :key="index">
        <el-button
          v-hasPerm="btn.perm ?? '*:*:*'"
          v-bind="btn.attrs"
          :disabled="btn.name === 'delete' && removeIds.length === 0"
          @click="$emit('toolbar', btn.name)"
        >
          {{ btn.text }}
        </el-button>
      </template>
    </template>
    <slot v-else>
      <el-button
        v-if="permCreate"
        v-hasPerm="permCreate"
        type="success"
        icon="plus"
        @click="$emit('add')"
      >
        新增
      </el-button>
      <el-button
        v-if="permDelete"
        v-hasPerm="permDelete"
        type="danger"
        icon="delete"
        :loading="deleteLoading"
        :disabled="removeIds.length === 0"
        @click="$emit('delete')"
      >
        批量删除
      </el-button>
      <el-dropdown v-if="permPatch" v-hasPerm="permPatch" trigger="click">
        <el-button
          type="default"
          :disabled="removeIds.length === 0 || moreDisabled"
          icon="ArrowDown"
        >
          更多
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item icon="Check" @click="$emit('more', '0')">批量启用</el-dropdown-item>
            <el-dropdown-item icon="CircleClose" @click="$emit('more', '1')">
              批量停用
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </slot>
  </div>
</template>

<script setup lang="ts">
  import { computed } from 'vue';
  import type { CrudToolbarConfigButton } from './types';

  const props = withDefaults(
    defineProps<{
      /** 与 PageContent `toolbarLeftBtn` 一致时走配置驱动（与 handleToolbar 对齐） */
      configButtons?: CrudToolbarConfigButton[];
      /** 勾选行主键，用于禁用批删 / 更多（插槽完全自定义时可不传） */
      removeIds?: Array<string | number>;
      /** 新增按钮权限，不传则不显示（configButtons 未传时） */
      permCreate?: string | string[];
      /** 批量删除权限，不传则不显示 */
      permDelete?: string | string[];
      /** 「更多」下拉权限，不传则不显示 */
      permPatch?: string | string[];
      /** 批量删除中（按钮 loading，并禁用「更多」） */
      deleteLoading?: boolean;
    }>(),
    {
      removeIds: () => [],
      deleteLoading: false,
    }
  );

  defineEmits<{
    /** 配置模式：与 PageContent handleToolbar 一致 */
    toolbar: [name: string];
    add: [];
    delete: [];
    more: [value: string];
  }>();

  const moreDisabled = computed(() => props.removeIds.length === 0 || props.deleteLoading);
</script>
