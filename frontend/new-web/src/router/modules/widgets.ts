import { AppRouteRecord } from "@/types/router";

export const widgetsRoutes: AppRouteRecord = {
  path: "/widgets",
  name: "Widgets",
  component: "/index/index",
  meta: {
    title: "menus.widgets.title",
    icon: "ri:apps-2-add-line",
  },
  children: [
    {
      path: "cards",
      name: "Cards",
      component: "/widgets/cards",
      meta: {
        title: "menus.widgets.cards",
        icon: "ri:wallet-line",
        keepAlive: false,
      },
    },
    {
      path: "banners",
      name: "Banners",
      component: "/widgets/banners",
      meta: {
        title: "menus.widgets.banners",
        icon: "ri:rectangle-line",
        keepAlive: false,
      },
    },
    {
      path: "charts",
      name: "Charts",
      component: "/widgets/charts",
      meta: {
        title: "menus.widgets.charts",
        icon: "ri:bar-chart-box-line",
        keepAlive: false,
      },
    },
    {
      path: "icon",
      name: "Icon",
      component: "/widgets/icon",
      meta: {
        title: "menus.widgets.icon",
        icon: "ri:palette-line",
        keepAlive: true,
      },
    },
    {
      path: "image-crop",
      name: "ImageCrop",
      component: "/widgets/image-crop",
      meta: {
        title: "menus.widgets.imageCrop",
        icon: "ri:screenshot-line",
        keepAlive: true,
      },
    },
    {
      path: "excel",
      name: "Excel",
      component: "/widgets/excel",
      meta: {
        title: "menus.widgets.excel",
        icon: "ri:download-2-line",
        keepAlive: true,
      },
    },
    {
      path: "video",
      name: "Video",
      component: "/widgets/video",
      meta: {
        title: "menus.widgets.video",
        icon: "ri:vidicon-line",
        keepAlive: true,
      },
    },
    {
      path: "count-to",
      name: "CountTo",
      component: "/widgets/count-to",
      meta: {
        title: "menus.widgets.countTo",
        icon: "ri:anthropic-line",
        keepAlive: false,
      },
    },
    {
      path: "wang-editor",
      name: "WangEditor",
      component: "/widgets/wang-editor",
      meta: {
        title: "menus.widgets.wangEditor",
        icon: "ri:t-box-line",
        keepAlive: true,
      },
    },
    {
      path: "watermark",
      name: "Watermark",
      component: "/widgets/watermark",
      meta: {
        title: "menus.widgets.watermark",
        icon: "ri:water-flash-line",
        keepAlive: true,
      },
    },
    {
      path: "context-menu",
      name: "ContextMenu",
      component: "/widgets/context-menu",
      meta: {
        title: "menus.widgets.contextMenu",
        icon: "ri:menu-2-line",
        keepAlive: true,
      },
    },
    {
      path: "qrcode",
      name: "Qrcode",
      component: "/widgets/qrcode",
      meta: {
        title: "menus.widgets.qrcode",
        icon: "ri:qr-code-line",
        keepAlive: true,
      },
    },
    {
      path: "drag",
      name: "Drag",
      component: "/widgets/drag",
      meta: {
        title: "menus.widgets.drag",
        icon: "ri:drag-move-fill",
        keepAlive: true,
      },
    },
    {
      path: "text-scroll",
      name: "TextScroll",
      component: "/widgets/text-scroll",
      meta: {
        title: "menus.widgets.textScroll",
        icon: "ri:input-method-line",
        keepAlive: true,
      },
    },
    {
      path: "fireworks",
      name: "Fireworks",
      component: "/widgets/fireworks",
      meta: {
        title: "menus.widgets.fireworks",
        icon: "ri:magic-line",
        keepAlive: true,
        showTextBadge: "Hot",
      },
    },

    /** 结果页（原 /result） */
    {
      path: "result",
      name: "Result",
      component: "",
      meta: {
        title: "menus.result.title",
        icon: "ri:checkbox-circle-line",
      },
      children: [
        {
          path: "success",
          name: "ResultSuccess",
          component: "/widgets/result/success",
          meta: {
            title: "menus.result.success",
            icon: "ri:checkbox-circle-line",
            keepAlive: true,
          },
        },
        {
          path: "fail",
          name: "ResultFail",
          component: "/widgets/result/fail",
          meta: {
            title: "menus.result.fail",
            icon: "ri:close-circle-line",
            keepAlive: true,
          },
        },
      ],
    },

    /** 功能示例（原 /examples） */
    {
      path: "examples",
      name: "Examples",
      component: "",
      meta: {
        title: "menus.examples.title",
        icon: "ri:sparkling-line",
      },
      children: [
        {
          path: "permission",
          name: "Permission",
          component: "",
          meta: {
            title: "menus.examples.permission.title",
            icon: "ri:fingerprint-line",
          },
          children: [
            {
              path: "switch-role",
              name: "PermissionSwitchRole",
              component: "/widgets/examples/permission/switch-role",
              meta: {
                title: "menus.examples.permission.switchRole",
                icon: "ri:contacts-line",
                keepAlive: true,
              },
            },
            {
              path: "button-auth",
              name: "PermissionButtonAuth",
              component: "/widgets/examples/permission/button-auth",
              meta: {
                title: "menus.examples.permission.buttonAuth",
                icon: "ri:mouse-line",
                keepAlive: true,
                authList: [
                  { title: "新增", authMark: "add" },
                  { title: "编辑", authMark: "edit" },
                  { title: "删除", authMark: "delete" },
                  { title: "导出", authMark: "export" },
                  { title: "查看", authMark: "view" },
                  { title: "发布", authMark: "publish" },
                  { title: "配置", authMark: "config" },
                  { title: "管理", authMark: "manage" },
                ],
              },
            },
            {
              path: "page-visibility",
              name: "PermissionPageVisibility",
              component: "/widgets/examples/permission/page-visibility",
              meta: {
                title: "menus.examples.permission.pageVisibility",
                icon: "ri:user-3-line",
                keepAlive: true,
                roles: ["R_SUPER"],
              },
            },
          ],
        },
        {
          path: "tabs",
          name: "Tabs",
          component: "/widgets/examples/tabs",
          meta: {
            title: "menus.examples.tabs",
            icon: "ri:price-tag-line",
          },
        },
        {
          path: "tables/basic",
          name: "TablesBasic",
          component: "/widgets/examples/tables/basic",
          meta: {
            title: "menus.examples.tablesBasic",
            icon: "ri:layout-grid-line",
            keepAlive: true,
          },
        },
        {
          path: "tables",
          name: "Tables",
          component: "/widgets/examples/tables",
          meta: {
            title: "menus.examples.tables",
            icon: "ri:table-3",
            keepAlive: true,
          },
        },
        {
          path: "forms",
          name: "Forms",
          component: "/widgets/examples/forms",
          meta: {
            title: "menus.examples.forms",
            icon: "ri:table-view",
            keepAlive: true,
          },
        },
        {
          path: "form/search-bar",
          name: "SearchBar",
          component: "/widgets/examples/forms/search-bar",
          meta: {
            title: "menus.examples.searchBar",
            icon: "ri:table-line",
            keepAlive: true,
          },
        },
        {
          path: "tables/tree",
          name: "TablesTree",
          component: "/widgets/examples/tables/tree",
          meta: {
            title: "menus.examples.tablesTree",
            icon: "ri:layout-2-line",
            keepAlive: true,
          },
        },
        {
          path: "socket-chat",
          name: "SocketChat",
          component: "/widgets/examples/socket-chat",
          meta: {
            title: "menus.examples.socketChat",
            icon: "ri:shake-hands-line",
            keepAlive: true,
          },
        },
      ],
    },

    /** 文章演示（原 /article） */
    {
      path: "article",
      name: "Article",
      component: "",
      meta: {
        title: "menus.article.title",
        icon: "ri:book-2-line",
        roles: ["R_SUPER", "R_ADMIN"],
      },
      children: [
        {
          path: "article-list",
          name: "ArticleList",
          component: "/widgets/article/list",
          meta: {
            title: "menus.article.articleList",
            icon: "ri:article-line",
            keepAlive: true,
            authList: [
              { title: "新增", authMark: "add" },
              { title: "编辑", authMark: "edit" },
            ],
          },
        },
        {
          path: "detail/:id",
          name: "ArticleDetail",
          component: "/widgets/article/detail",
          meta: {
            title: "menus.article.articleDetail",
            isHide: true,
            keepAlive: true,
            activePath: "/widgets/article/article-list",
          },
        },
        {
          path: "comment",
          name: "ArticleComment",
          component: "/widgets/article/comment",
          meta: {
            title: "menus.article.comment",
            icon: "ri:mail-line",
            keepAlive: true,
          },
        },
        {
          path: "publish",
          name: "ArticlePublish",
          component: "/widgets/article/publish",
          meta: {
            title: "menus.article.articlePublish",
            icon: "ri:telegram-2-line",
            keepAlive: true,
            authList: [{ title: "发布", authMark: "add" }],
          },
        },
      ],
    },

    /** 更新日志（原 views/change/log） */
    {
      path: "change",
      name: "Change",
      component: "",
      meta: {
        title: "menus.widgets.changeLog",
        icon: "ri:gamepad-line",
      },
      children: [
        {
          path: "log",
          name: "ChangeLog",
          component: "/widgets/change/log",
          meta: {
            title: "menus.widgets.changeLog",
            icon: "ri:gamepad-line",
            keepAlive: true,
          },
        },
      ],
    },
  ],
};
