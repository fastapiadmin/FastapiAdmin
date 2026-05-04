<!-- 角色授权 -->
<template>
  <ArtDrawer
    v-model="drawerVisible"
    :title="'【' + props.roleName + '】权限分配'"
    :size="drawerSize"
    destroy-on-close
    @close="handleCancel"
  >
    <div class="drawer-perm-content flex flex-col min-h-0 flex-1 overflow-hidden">
      <ElContainer class="h-full min-h-0 flex-1">
        <!-- 数据权限 -->
        <ElAside>
          <div
            class="border-r-1 border-r-[var(--el-border-color-lighter)] b-r-solid h-[100%] p-[20px] box-border"
          >
            <div class="flex items-center">
              <div style="display: flex; gap: 10px">
                <div style="width: 10px; background-color: var(--el-color-primary)"></div>
                <div>
                  <span style="font-size: 16px">数据授权</span>
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

              <div
                v-if="permissionState.data_scope === 5 && deptTreeData.length"
                class="mt-5 max-h-[60vh] b-1 b-solid b-[var(--el-border-color-lighter)] p-10px overflow-auto box-border"
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
                  :check-strictly="!parentChildLinked"
                  style="height: calc(100% - 60px); margin-top: 10px; overflow-y: auto"
                  @check="deptTreeCheck"
                >
                  <template #empty>
                    <ElEmpty :image-size="80" description="暂无数据" />
                  </template>
                </ElTree>
              </div>
            </div>
          </div>
        </ElAside>

        <!-- 菜单权限 -->
        <ElMain>
          <div style="display: flex; gap: 10px">
            <div style="width: 10px; background-color: var(--el-color-primary)"></div>
            <div>
              <span style="font-size: 16px">菜单授权</span>
              <ElTooltip placement="right">
                <template #content>
                  <span>授权用户可操作的菜单权限</span>
                </template>
                <ElIcon class="ml-1 inline-block cursor-pointer">
                  <QuestionFilled />
                </ElIcon>
              </ElTooltip>
            </div>
          </div>
          <div class="mt-3 flex-x-between">
            <ElInput v-model="permFilterText" placeholder="菜单名称" />
            <div class="flex-center ml-5">
              <ElButton type="primary" size="small" plain @click="togglePermTree">
                <template #icon>
                  <SwitchIcon />
                </template>
                {{ isExpanded ? "收缩" : "展开" }}
              </ElButton>
              <ElCheckbox
                v-model="parentChildLinked"
                class="ml-5"
                @change="handleParentChildLinkedChange"
              >
                父子联动
              </ElCheckbox>

              <ElTooltip placement="bottom">
                <template #content>
                  如果只需勾选菜单权限，不需要勾选子菜单或者按钮权限，请关闭父子联动
                </template>
                <ElIcon class="ml-1 color-[--el-color-primary] inline-block cursor-pointer">
                  <QuestionFilled />
                </ElIcon>
              </ElTooltip>
            </div>
          </div>

          <div
            class="mt-5 max-h-[69vh] b-1 b-solid b-[var(--el-border-color-lighter)] p-10px overflow-auto box-border"
          >
            <ElTree
              ref="permTreeRef"
              node-key="value"
              show-checkbox
              :data="menuTreeData"
              :filter-node-method="handleFilter"
              default-expand-all
              :highlight-current="true"
              :check-strictly="!parentChildLinked"
              style="height: calc(100% - 60px); margin-top: 10px; overflow: auto"
              @check="menuTreeCheck"
            >
              <template #empty>
                <ElEmpty :image-size="80" description="暂无数据" />
              </template>
            </ElTree>
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
  </ArtDrawer>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from "vue";
import { QuestionFilled, Switch as SwitchIcon } from "@element-plus/icons-vue";
import type { TreeInstance } from "element-plus";
import ArtDrawer from "@/components/Core/modal/art-drawer/index.vue";
import { listToTree, formatTree } from "@/utils/common";
import RoleAPI, {
  permissionDataType,
  permissionDeptType,
  permissionMenuType,
} from "@/api/module_system/role";
import DeptAPI from "@/api/module_system/dept";
import MenuAPI from "@/api/module_system/menu";
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { useUserStore } from "@/store";

/** formatTree 后的菜单节点带 value（同原 id），与接口里的 id 二选一存在 */
type MenuTreeNode = permissionMenuType & { value?: number };

const props = defineProps<{
  roleName: string;
  roleId: number;
  modelValue: boolean;
}>();

const emit = defineEmits<{
  "update:modelValue": [v: boolean];
  saved: [];
}>();

const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "800px" : "90%"));

const drawerVisible = computed({
  get() {
    return props.modelValue;
  },
  set(value: boolean) {
    emit("update:modelValue", value);
  },
});

const permTreeRef = ref<TreeInstance>();
const deptTreeRef = ref<TreeInstance>();
const deptFilterText = ref("");
const permFilterText = ref("");
const dataFormRef = ref();
const isExpanded = ref(true);
const parentChildLinked = ref(false);
const loading = ref(false);
const deptTreeData = ref<permissionDeptType[]>([]);
const menuTreeData = ref<MenuTreeNode[]>([]);
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
    menuTreeData.value = formatTree(listToTree(menuResponse.data.data));

    const roleResponse = await RoleAPI.detailRole(props.roleId);

    permissionState.value = {
      role_ids: [props.roleId],
      menu_ids: roleResponse.data.data.menus?.map((menu) => menu.id) || [],
      data_scope: roleResponse.data.data.data_scope || 1,
      dept_ids: roleResponse.data.data.depts?.map((dept) => dept.id) || [],
    };

    parentChildLinked.value = checkParentChildLinked(
      permissionState.value.menu_ids,
      menuTreeData.value
    );

    if (permTreeRef.value) {
      await permTreeRef.value.setCheckedKeys(permissionState.value.menu_ids);
    }

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

    const rawChecked = (permTreeRef.value?.getCheckedKeys() || []).map((key) => Number(key));
    const menu_ids = expandMenuIdsWithAncestors(rawChecked, menuTreeData.value);

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

const menuTreeCheck = (checkedIds: number[]) => {
  permissionState.value.menu_ids = checkedIds;
};

function togglePermTree() {
  isExpanded.value = !isExpanded.value;
  if (permTreeRef.value) {
    Object.values(permTreeRef.value.store.nodesMap).forEach((node: any) => {
      if (isExpanded.value) {
        node.expand();
      } else {
        node.collapse();
      }
    });
  }
}

watch(deptFilterText, (val) => {
  deptTreeRef.value!.filter(val);
});

watch(permFilterText, (val) => {
  permTreeRef.value!.filter(val);
});

function handleFilter(value: string, data: { [key: string]: any }) {
  if (!value) return true;
  return data.label.includes(value);
}

function menuTreeNodeId(node: MenuTreeNode): number {
  const v = node.value ?? node.id;
  return Number(v);
}

function checkParentChildLinked(menuIds: number[], menuTreeData: MenuTreeNode[]): boolean {
  if (!menuIds.length || !menuTreeData.length) return false;

  const menuMap = new Map<number, MenuTreeNode>();
  const buildMenuMap = (menus: MenuTreeNode[]) => {
    menus.forEach((menu) => {
      menuMap.set(menuTreeNodeId(menu), menu);
      if (menu.children) {
        buildMenuMap(menu.children as MenuTreeNode[]);
      }
    });
  };
  buildMenuMap(menuTreeData);

  let hasParentChildConflict = false;

  for (const menuId of menuIds) {
    const menu = menuMap.get(menuId);
    if (!menu) continue;

    if (menu.children && menu.children.length > 0) {
      const hasUnselectedChildren = menu.children.some(
        (child) => !menuIds.includes(menuTreeNodeId(child as MenuTreeNode))
      );
      if (hasUnselectedChildren) {
        hasParentChildConflict = true;
        break;
      }
    }

    const parentMenu = findParentMenu(menuId, menuTreeData);
    if (parentMenu && !menuIds.includes(menuTreeNodeId(parentMenu))) {
      hasParentChildConflict = true;
      break;
    }
  }

  return !hasParentChildConflict;
}

function findParentMenu(menuId: number, menuTreeData: MenuTreeNode[]): MenuTreeNode | null {
  for (const menu of menuTreeData) {
    if (menu.children) {
      for (const child of menu.children) {
        if (menuTreeNodeId(child as MenuTreeNode) === menuId) {
          return menu;
        }
        const found = findParentMenu(menuId, [child as MenuTreeNode]);
        if (found) return found;
      }
    }
  }
  return null;
}

/** 为已选菜单补齐所有祖先 id，避免仅选子节点时父级未入库导致侧栏/路由缺入口（BUG #1/#14） */
function expandMenuIdsWithAncestors(checkedIds: number[], roots: MenuTreeNode[]): number[] {
  const parentById = new Map<number, number | undefined>();
  const walk = (nodes: MenuTreeNode[], parent: number | undefined) => {
    for (const n of nodes) {
      const id = menuTreeNodeId(n);
      parentById.set(id, parent);
      if (n.children?.length) walk(n.children as MenuTreeNode[], id);
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

function handleParentChildLinkedChange(val: any) {
  parentChildLinked.value = val;
}

onMounted(async () => {
  await init();
});
</script>

<style lang="scss" scoped></style>
