<!-- 角色授权 -->
<template>
  <FaDrawer
    v-model="drawerVisible"
    :title="'【' + props.roleName + '】权限分配'"
    :size="drawerSize"
    destroy-on-close
    @close="handleCancel"
  >
    <div class="drawer-perm-content flex flex-col flex-1 overflow-hidden">
      <ElContainer class="h-full min-h-0 flex-1">
        <!-- 数据权限 -->
        <ElAside>
          <div
            class="border-r border-r-(--el-border-color-lighter) b-r-solid h-full p-[20px] box-border"
          >
            <div class="flex items-center">
              <div class="flex gap-[10px]">
                <div class="w-[10px] bg-(--el-color-primary)"></div>
                <div>
                  <span class="text-[16px]">数据授权</span>
                  <ElTooltip placement="right">
                    <template #content>
                      <span>授权用户可操作的数据范围</span>
                    </template>
                    <ElIcon class="ml-1 inline-block cursor-pointer">
                      <QuestionFilled />
                    </ElIcon>
                  </ElTooltip>
                </div>
              </div>
            </div>
            <div class="mt-3">
              <ElForm ref="dataFormRef" :model="permissionState">
                <ElFormItem prop="data_scope">
                  <ElSelect v-model="permissionState.data_scope">
                    <ElOption :key="1" label="仅本人数据权限" :value="1" />
                    <ElOption :key="2" label="本部门数据权限" :value="2" />
                    <ElOption :key="3" label="本部门及以下数据权限" :value="3" />
                    <ElOption :key="4" label="全部数据权限" :value="4" />
                    <ElOption :key="5" label="自定义数据权限" :value="5" />
                  </ElSelect>
                </ElFormItem>
              </ElForm>

              <ElScrollbar
                v-if="permissionState.data_scope === 5 && deptTreeData.length"
                class="mt-5 max-h-[72vh] b-1 b-solid b-[var(--el-border-color-lighter)] p-10px box-border"
              >
                <ElInput v-model="deptFilterText" placeholder="部门名称" />
                <ElTree
                  ref="deptTreeRef"
                  node-key="value"
                  show-checkbox
                  :data="deptTreeData"
                  :filter-node-method="handleFilter"
                  default-expand-all
                  :highlight-current="true"
                  :style="'height: calc(100% - 60px); margin-top: 10px'"
                  @check="deptTreeCheck"
                >
                  <template #empty>
                    <ElEmpty :image-size="80" description="暂无数据" />
                  </template>
                </ElTree>
              </ElScrollbar>
            </div>
          </div>
        </ElAside>

        <!-- 菜单权限 -->
        <ElMain>
          <div class="flex gap-[10px]">
            <div class="w-[10px] bg-(--el-color-primary)"></div>
            <div>
              <span class="text-[16px]">菜单授权</span>
              <ElTooltip placement="right">
                <template #content>
                  <span>勾选菜单和对应的功能按钮权限</span>
                </template>
                <ElIcon class="ml-1 inline-block cursor-pointer">
                  <QuestionFilled />
                </ElIcon>
              </ElTooltip>
            </div>
          </div>
          <div class="mt-3 flex-1 min-h-0">
            <FaMenuTreeTable
              ref="menuTreeTableRef"
              :menu-tree="rawMenuTree"
              :checked-ids="menuCheckedIds"
              :loading="loading"
            />
          </div>
        </ElMain>
      </ElContainer>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <ElButton @click="handleCancel">取 消</ElButton>
        <ElButton type="primary" :loading="loading" @click.stop="handleDrawerSave">确 定</ElButton>
      </div>
    </template>
  </FaDrawer>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, nextTick } from "vue";
import { QuestionFilled } from "@element-plus/icons-vue";
import type { TreeInstance } from "element-plus";
import { listToTree, formatTree, type CascaderNode } from "@utils";
import FaMenuTreeTable from "@/components/others/fa-menu-tree-table/index.vue";
import RoleAPI, { permissionDataType } from "@/api/module_system/role";
import DeptAPI from "@/api/module_system/dept";
import MenuAPI, { MenuTable } from "@/api/module_platform/menu";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { useAppStore, useUserStore } from "@stores";
import { ElMessage } from "element-plus";

const props = defineProps<{
  roleName: string;
  roleId: number;
  modelValue: boolean;
}>();

interface Emits {
  "update:modelValue": [v: boolean];
  saved: [];
}

const emit = defineEmits<Emits>();

const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "1200px" : "90%"));

const drawerVisible = computed({
  get: () => props.modelValue,
  set(v) {
    emit("update:modelValue", v);
  },
});

const deptTreeRef = ref<TreeInstance>();
const deptFilterText = ref("");
const dataFormRef = ref();
const loading = ref(false);
const deptTreeData = ref<CascaderNode[]>([]);
const rawMenuTree = ref<MenuTable[]>([]);
const menuCheckedIds = ref<number[]>([]);
const menuTreeTableRef = ref<InstanceType<typeof FaMenuTreeTable>>();

const permissionState = ref<permissionDataType>({
  role_ids: [],
  menu_ids: [],
  data_scope: 1,
  dept_ids: [],
});

const init = async () => {
  loading.value = true;
  try {
    const deptResponse = await DeptAPI.listDept();
    deptTreeData.value = formatTree(listToTree(deptResponse.data.data));

    const menuResponse = await MenuAPI.listMenu();
    rawMenuTree.value = menuResponse.data.data || [];

    const roleResponse = await RoleAPI.detailRole(props.roleId);
    const savedMenuIds = roleResponse.data.data.menus?.map((menu: any) => menu.id) || [];

    permissionState.value = {
      role_ids: [props.roleId],
      menu_ids: savedMenuIds,
      data_scope: roleResponse.data.data.data_scope || 1,
      dept_ids: roleResponse.data.data.depts?.map((dept: any) => dept.id) || [],
    };

    menuCheckedIds.value = savedMenuIds;

    await nextTick();

    if (permissionState.value.data_scope === 5 && deptTreeRef.value) {
      await deptTreeRef.value.setCheckedKeys(permissionState.value.dept_ids);
    }
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : String(error);
    ElMessage.error("获取权限数据失败: " + msg);
  } finally {
    loading.value = false;
  }
};

function handleCancel() {
  drawerVisible.value = false;
}

async function handleDrawerSave() {
  try {
    if (props.roleId === 1) {
      ElMessage.warning("系统默认角色，不可操作");
      return;
    }
    loading.value = true;

    const checkedIds = menuTreeTableRef.value?.getCheckedIds() ?? [];
    const menu_ids = expandMenuIdsWithAncestors(checkedIds, rawMenuTree.value);

    const submitData: permissionDataType = {
      role_ids: [props.roleId],
      menu_ids,
      data_scope: permissionState.value.data_scope,
      dept_ids: (deptTreeRef.value?.getCheckedKeys() || []).map((key) => Number(key)),
    };

    await RoleAPI.setPermission(submitData);

    const userStore = useUserStore();
    await userStore.getUserInfo();

    drawerVisible.value = false;
    emit("saved");
  } catch (error: unknown) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

const deptTreeCheck = (checkedIds: number[]) => {
  permissionState.value.dept_ids = checkedIds;
};

function handleFilter(value: string, data: { [key: string]: any }) {
  if (!value) return true;
  return data.label?.includes(value);
}

/** 将选中的菜单/按钮 ID 展开为包含所有祖先菜单的完整集合 */
function expandMenuIdsWithAncestors(checkedIds: number[], roots: MenuTable[]): number[] {
  const parentById = new Map<number, number | undefined>();
  const walk = (nodes: MenuTable[], parent: number | undefined) => {
    for (const n of nodes) {
      const id = n.id!;
      parentById.set(id, parent);
      if (n.children?.length) walk(n.children as MenuTable[], id);
    }
  };
  walk(roots, undefined);
  const out = new Set<number>();
  for (const id of checkedIds) {
    let cur: number | undefined = id;
    while (cur !== undefined) {
      out.add(cur);
      cur = parentById.get(cur);
    }
  }
  return [...out];
}

watch(deptFilterText, (val) => {
  deptTreeRef.value!.filter(val);
});

onMounted(async () => {
  await init();
});
</script>
