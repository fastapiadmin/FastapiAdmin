import type { App } from 'vue';
import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router';
import { staticRoutes } from './routes/staticRoutes';
import { configureNProgress } from '@/utils/router';
import { setupBeforeEachGuard } from './guards/beforeEach';
import { setupAfterEachGuard } from './guards/afterEach';

export const Layout = () => import('@/layouts/index.vue');
/**
 * 静态路由
 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: '/redirect',
    meta: { hidden: true },
    component: Layout,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index.vue'),
      },
    ],
  },
  {
    path: '/login',
    name: 'Login',
    meta: { hidden: true },
    component: () => import('@/views/module_system/auth/index.vue'),
  },
  {
    path: '/401',
    name: '401',
    meta: { hidden: true, title: '401' },
    component: () => import('@/views/error/401.vue'),
  },
  {
    path: '/404',
    name: '404',
    meta: { hidden: true, title: '404' },
    component: () => import('@/views/error/404.vue'),
  },
  {
    path: '/500',
    name: '500',
    meta: { hidden: true, title: '500' },
    component: () => import('@/views/error/500.vue'),
  },
  {
    path: '/',
    name: '/',
    redirect: '/home',
    component: Layout,
    children: [
      {
        path: 'home',
        component: () => import('@/views/dashboard/index.vue'),
        // 用于 keep-alive 功能，需要与 SFC 中自动推导或显式声明的组件名称一致
        // 参考文档: https://cn.vuejs.org/guide/built-ins/keep-alive.html#include-exclude
        name: 'Home',
        meta: {
          title: '首页',
          icon: 'homepage',
          affix: true,
          keepAlive: true,
        },
      },
      {
        path: 'profile',
        name: 'Profile',
        meta: { title: '个人中心', icon: 'user', hidden: true },
        component: () => import('@/views/current/profile.vue'),
      },
    ],
  },
  // 通配 404 必须置于静态路由最后，否则会抢先匹配 /、/home 等
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/error/404.vue'),
    meta: { hidden: true, title: '404' },
  },
];

/**
 * 创建路由
 */
const router = createRouter({
  history: createWebHashHistory(),
  routes: constantRoutes.concat(staticRoutes), // 静态路由
  // 刷新时，滚动条位置还原
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

// 全局注册 router
// 为了捕获并处理全局错误，在注册路由时添加错误处理
// 初始化路由
export function initRouter(app: App<Element>): void {
  configureNProgress(); // 顶部进度条
  setupBeforeEachGuard(router); // 路由前置守卫
  setupAfterEachGuard(router); // 路由后置守卫
  app.use(router);
}

export default router;

// 主页路径，默认使用菜单第一个有效路径，配置后使用此路径
export const HOME_PAGE_PATH = '';
