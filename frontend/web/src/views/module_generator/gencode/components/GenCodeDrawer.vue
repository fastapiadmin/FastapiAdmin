<template>
  <EnhancedDrawer
    v-model="drawerVisible"
    :title="'【代码生成】' + (info.table_name || '')"
    size="90%"
    drawer-class="gencode-drawer"
    append-to-body
    @close="emit('close')"
  >
    <el-steps :active="activeStep" finish-status="success" simple>
      <el-step title="基础配置" />
      <el-step title="字段配置" />
      <el-step title="预览代码" />
    </el-steps>

    <div class="gencode-drawer-step-wrap mt-4">
      <div v-show="activeStep === 0">
        <GenBasicStep
          :info="info"
          :rules="rules"
          :menu-options="menuOptions"
          @clear-master-sub="emit('clear-master-sub')"
          @master-sub-blur="emit('master-sub-blur')"
        />
      </div>

      <div v-show="activeStep === 1">
        <GenColumnsStep
          :info="info"
          :dict-options="dictOptions"
          :loading="loading"
          :bulk-set="bulkSet"
        />
      </div>

      <GenPreviewStep
        v-show="activeStep === 2"
        v-model:preview-scope="previewScope"
        v-model:preview-types="previewTypes"
        v-model:code="code"
        :preview-loading="previewLoading"
        :preview-type-options="previewTypeOptions"
        :filtered-tree-data="filteredTreeData"
        :cm-options="cmOptions"
        @file-click="emit('file-click', $event)"
        @copy-code="emit('copy-code')"
      />
    </div>

    <template #footer>
      <el-button :icon="Close" @click="emit('close')">关闭</el-button>
      <el-button
        v-if="activeStep < 2"
        type="info"
        :icon="Finished"
        :loading="loading"
        @click="emit('save')"
      >
        保存
      </el-button>
      <el-button v-if="activeStep !== 0" type="success" :icon="Back" @click="emit('prev-step')">
        上一步
      </el-button>
      <el-button
        v-if="activeStep !== 2"
        type="primary"
        :loading="nextStepLoading"
        @click="emit('next-step')"
      >
        {{ nextStepButtonLabel }}
        <el-icon class="el-icon--right"><Right /></el-icon>
      </el-button>
      <el-tooltip
        v-if="activeStep === 2"
        content="打包为 ZIP 下载到本机，不会在服务器创建菜单或文件"
        placement="top"
      >
        <el-button type="warning" :icon="Download" :loading="loading" @click="emit('gen-download')">
          下载代码
        </el-button>
      </el-tooltip>
      <el-tooltip
        v-if="activeStep === 2"
        content="在服务端项目目录生成源码，并自动创建目录/菜单/按钮（若名称未冲突）"
        placement="top"
      >
        <el-button
          type="primary"
          :icon="FolderOpened"
          :loading="loading"
          @click="emit('gen-write')"
        >
          写入本地
        </el-button>
      </el-tooltip>
    </template>
  </EnhancedDrawer>
</template>

<script setup lang="ts">
  import { computed } from 'vue';
  import type { FormRules } from 'element-plus';
  import { Close, Right, FolderOpened, Back, Download, Finished } from '@element-plus/icons-vue';
  import type { EditorConfiguration } from 'codemirror';
  import type { GenTableSchema } from '@/api/module_generator/gencode';
  import type { DictTable } from '@/api/module_system/dict';
  import EnhancedDrawer from '@/components/CURD/EnhancedDrawer.vue';
  import type { TreeNode } from '../types';
  import GenBasicStep from './GenBasicStep.vue';
  import GenColumnsStep from './GenColumnsStep.vue';
  import GenPreviewStep from './GenPreviewStep.vue';

  defineOptions({ name: 'GenCodeDrawer' });

  const props = defineProps<{
    info: GenTableSchema;
    rules: FormRules;
    activeStep: number;
    menuOptions: OptionType[];
    dictOptions: DictTable[];
    loading: boolean;
    nextStepLoading: boolean;
    previewLoading: boolean;
    previewTypeOptions: string[];
    filteredTreeData: TreeNode[];
    cmOptions: EditorConfiguration;
    bulkSet: (field: string | string[], value: unknown) => void;
  }>();

  const nextStepButtonLabel = computed(() =>
    props.activeStep === 0 ? '下一步：字段配置' : '下一步：预览代码'
  );

  const drawerVisible = defineModel<boolean>({ required: true });

  const previewScope = defineModel<'all' | 'frontend' | 'backend'>('previewScope', {
    required: true,
  });
  const previewTypes = defineModel<string[]>('previewTypes', { required: true });
  const code = defineModel<string>('code', { required: true });

  const emit = defineEmits<{
    close: [];
    'prev-step': [];
    'next-step': [];
    save: [];
    'gen-download': [];
    'gen-write': [];
    'clear-master-sub': [];
    'master-sub-blur': [];
    'file-click': [data: TreeNode];
    'copy-code': [];
  }>();
</script>

<style scoped lang="scss">
  /* 新版 ElDrawer 内部用 Splitter，size 需为百分比或纯数字(px)，勿用 min()，否则面板宽度可能异常 */
  .gencode-drawer-step-wrap {
    max-height: calc(100vh - 220px);
    padding-right: 6px;
    overflow-x: hidden;
    overflow-y: auto;
  }
</style>
