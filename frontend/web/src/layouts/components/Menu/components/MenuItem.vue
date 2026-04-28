<template>
  <div v-if="!item.meta || !item.meta.hidden">
    <!--【叶子节点】显示叶子节点或唯一子节点且父节点未配置始终显示 -->
    <template
      v-if="
        // 未配置始终显示，使用唯一子节点替换父节点显示为叶子节点
        (hasOneShowingChild(item.children, item) &&
          !item.meta?.alwaysShow &&
          (!onlyOneChild.children || onlyOneChild.noShowingChildren)) ||
        // 即使配置了始终显示，但无子节点，也显示为叶子节点
        (item.meta?.alwaysShow && !item.children)
      "
    >
      <AppLink
        v-if="onlyOneChild.meta"
        :to="
          onlyOneChild.name
            ? { name: onlyOneChild.name, query: onlyOneChild.meta.params }
            : { path: resolvePath(onlyOneChild.path || ''), query: onlyOneChild.meta.params }
        "
      >
        <el-menu-item
          :index="menuItemIndex(onlyOneChild, resolvePath(onlyOneChild.path || ''))"
          :class="{ 'submenu-title-noDropdown': !isNest }"
        >
          <MenuItemContent
            v-if="onlyOneChild.meta"
            :icon="onlyOneChild.meta.icon || item.meta?.icon"
            :title="onlyOneChild.meta.title"
          />
        </el-menu-item>
      </AppLink>
    </template>

    <!--【非叶子节点】显示含多个子节点的父菜单，或始终显示的单子节点 -->
    <el-sub-menu
      v-else
      :index="menuItemIndex(item, resolvePath(item.path || ''))"
      :data-path="resolvePath(item.path || '')"
    >
      <template #title>
        <span class="menu-title-wrapper" :data-path="resolvePath(item.path || '')">
          <MenuItemContent v-if="item.meta" :icon="item.meta.icon" :title="item.meta.title" />
        </span>
      </template>

      <MenuItem
        v-for="child in item.children"
        :key="String(child.name ?? child.path)"
        :is-nest="true"
        :item="child"
        :base-path="resolvePath(item.path || '')"
      />
    </el-sub-menu>
  </div>
</template>

<script setup lang="ts">
  import MenuItemContent from './MenuItemContent.vue';

  defineOptions({
    name: 'MenuItem',
    inheritAttrs: false,
  });

  import path from 'path-browserify';
  import { RouteRecordRaw } from 'vue-router';
  import { useRouter } from 'vue-router';

  import { isExternal } from '@/utils';

  const router = useRouter();

  const props = defineProps({
    /**
     * 当前路由对象
     */
    item: {
      type: Object as PropType<RouteRecordRaw>,
      required: true,
    },

    /**
     * 父级完整路径
     */
    basePath: {
      type: String,
      required: true,
    },

    /**
     * 是否为嵌套路由
     */
    isNest: {
      type: Boolean,
      default: false,
    },
  });

  // 可见的唯一子节点
  const onlyOneChild = ref();

  /**
   * 检查是否仅有一个可见子节点
   *
   * @param children 子路由数组
   * @param parent 父级路由
   * @returns 是否仅有一个可见子节点
   */
  function hasOneShowingChild(children: RouteRecordRaw[] = [], parent: RouteRecordRaw) {
    // 过滤出可见子节点
    const showingChildren = children.filter((route: RouteRecordRaw) => {
      if (!route.meta?.hidden) {
        onlyOneChild.value = route;
        return true;
      }
      return false;
    });

    // 仅有一个节点
    if (showingChildren.length === 1) {
      return true;
    }

    // 无子节点时
    if (showingChildren.length === 0) {
      // 父节点设置为唯一显示节点，并标记为无子节点
      onlyOneChild.value = { ...parent, path: '', noShowingChildren: true };
      return true;
    }
    return false;
  }

  /**
   * 获取完整路径，适配外部链接
   *
   * @param routePath 路由路径
   * @returns 绝对路径
   */
  function resolvePath(routePath: string) {
    if (isExternal(routePath)) return routePath;
    if (isExternal(props.basePath)) return props.basePath;

    const base = props.basePath && props.basePath !== '' ? props.basePath : '/';
    return path.resolve(base, routePath);
  }

  /** 与 BasicMenu.default-active（route.path）对齐 */
  function normalizeMenuPath(p: string): string {
    if (!p) return '';
    if (/^https?:\/\//i.test(p) || p.startsWith('//')) return p;
    const s = p.trim();
    if (s === '/') return '/';
    return s.replace(/\/+$/, '') || '/';
  }

  function hasVisibleChildren(node: RouteRecordRaw): boolean {
    return !!node.children?.some((c) => !c.meta?.hidden);
  }

  /**
   * el-menu 的 index 必须与 default-active 字符串完全一致。
   * - 目录（有可见子节点）：只用菜单树 path.resolve 结果，禁止 router.resolve(name)（常变成父级 /task，导致兄弟目录误亮）。
   * - 叶子：用 router.resolve(name).path，与当前页 route.path 同源，避免纯拼路径与路由表不一致。
   */
  function menuItemIndex(item: RouteRecordRaw, resolvedFromTree: string): string {
    const treePath = normalizeMenuPath(resolvedFromTree);

    if (hasVisibleChildren(item)) {
      if (treePath) return treePath;
      if (item.name != null && item.name !== '') return String(item.name);
      return '';
    }

    if (item.name) {
      try {
        return normalizeMenuPath(router.resolve({ name: item.name as string }).path);
      } catch {
        /* fallthrough */
      }
    }
    return treePath;
  }
</script>

<style lang="scss">
  .hideSidebar {
    .submenu-title-noDropdown {
      position: relative;

      & > span {
        display: inline-block;
        visibility: hidden;
        width: 0;
        height: 0;
        overflow: hidden;
      }
    }

    .el-sub-menu {
      overflow: hidden;

      & > .el-sub-menu__title {
        .sub-el-icon {
          margin-left: 19px;
        }

        .el-sub-menu__icon-arrow {
          display: none;
        }
      }
    }

    .el-menu--collapse {
      width: $sidebar-width-collapsed;

      .el-sub-menu {
        & > .el-sub-menu__title > span {
          display: inline-block;
          visibility: hidden;
          width: 0;
          height: 0;
          overflow: hidden;
        }
      }
    }
  }

  // 父菜单激活状态样式 - 当子菜单激活时，父菜单显示激活状态
  .el-sub-menu {
    .menu-title-wrapper {
      display: inline-flex;
      align-items: center;
      height: 100%;
      line-height: 1;
    }

    // 子项激活时 Element Plus 会给父级 el-sub-menu 加 .is-active
    &.is-active > .el-sub-menu__title {
      color: var(--el-color-primary) !important;

      .menu-icon {
        color: var(--el-color-primary) !important;
      }
    }

    html.dark & {
      &.is-active > .el-sub-menu__title {
        color: var(--el-color-primary-light-3) !important;

        .menu-icon {
          color: var(--el-color-primary-light-3) !important;
        }
      }
    }

    html.sidebar-color-blue & {
      &.is-active > .el-sub-menu__title {
        color: var(--el-color-primary-light-3) !important;

        .menu-icon {
          color: var(--el-color-primary-light-3) !important;
        }
      }
    }
  }
</style>
