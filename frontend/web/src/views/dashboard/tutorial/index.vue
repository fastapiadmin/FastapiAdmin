<!-- 操作教程：内置视频演示（可改为自有 CDN / 资源地址） -->
<template>
  <div class="page-content tutorial-page">
    <div class="max-w-200 mx-auto">
      <h1 class="text-2xl font-medium text-g-900 dark:text-g-50 mb-2">操作教程</h1>
      <p class="text-sm text-g-600 mb-6">
        以下为系统常用操作演示视频，可随时暂停、调速与全屏观看。正式环境请将视频地址替换为自有素材。
      </p>

      <!-- Tab 切换：视频 / 手册 -->
      <ElTabs v-model="activeTab" class="manual-page__tabs">
        <!-- 视频演示 Tab -->
        <ElTabPane :label="t('manualPage.videoTab')" name="video">
          <div class="art-card-sm mt-2 p-5">
            <p class="mb-4 text-sm text-g-600 dark:text-g-400">
              {{ t("manualPage.videoHint") }}
            </p>
            <div class="manual-page__player max-w-full">
              <ArtVideoPlayer
                :player-id="PLAYER_ID"
                :video-url="videoUrl"
                :poster-url="posterUrl"
                :autoplay="false"
                :volume="1"
                :playback-rates="[0.5, 1, 1.5, 2]"
              />
            </div>
          </div>
        </ElTabPane>

        <!-- 功能验收手册 Tab -->
        <ElTabPane :label="t('manualPage.manualTab')" name="manual">
          <p class="mb-3 mt-2 text-sm text-g-600 dark:text-g-400">
            {{ t("manualPage.manualHint") }}
          </p>

          <div class="manual-feature-body">
            <!-- 工具栏：筛选 -->
            <div class="manual-feature-body__toolbar">
              <ElInput
                v-model="tocFilter"
                clearable
                placeholder="筛选目录…"
                :prefix-icon="Search"
                class="manual-feature-body__filter"
              />
            </div>

            <!-- 主体布局：侧边导航 + 内容区 -->
            <div class="manual-feature-body__layout">
              <!-- 左侧目录（不用 ElAffix：固钉时 fixed 宽度易丢失成窄条叠在主内容上；与右侧滚动区并排即可始终可见） -->
              <aside class="manual-feature-body__aside" aria-label="手册导航">
                <nav v-if="filteredToc.length" class="manual-nav">
                  <div v-for="mod in filteredToc" :key="mod.anchor" class="manual-nav__module">
                    <ElButton
                      link
                      type="primary"
                      class="manual-nav__mod-title !h-auto min-h-0 justify-start px-0 py-1"
                      @click="scrollToAnchor(mod.anchor)"
                    >
                      {{ mod.title }}
                    </ElButton>
                    <div class="manual-nav__pages">
                      <ElButton
                        v-for="p in mod.pages"
                        :key="p.anchor"
                        link
                        size="small"
                        class="manual-nav__page !h-auto min-h-0 justify-start px-2 py-1"
                        @click="scrollToAnchor(p.anchor)"
                      >
                        {{ p.title }}
                      </ElButton>
                    </div>
                  </div>
                </nav>
                <div v-else class="manual-nav manual-nav--empty">
                  <ElEmpty description="无匹配目录" :image-size="64" />
                </div>
              </aside>

              <!-- 右侧内容区（滚动） -->
              <ElScrollbar
                ref="scrollbarRef"
                class="manual-feature-body__scrollbar art-card-sm rounded-custom-sm"
                max-height="min(78vh, 880px)"
              >
                <!-- 功能验收手册正文内容 -->
                <div class="manual-html" @click.capture="handleAnchorClick">
                  <div class="manual-html__inner">
                    <h1>
                      FastapiAdmin 功能点清单
                      <small>用于全功能测试验收，按模块逐页列出所有可操作元素</small>
                    </h1>

                    <!-- 目录 -->
                    <ElCard id="toc" shadow="never" class="toc mb-6">
                      <template #header>
                        <span class="text-base font-medium">📋 目录</span>
                      </template>
                      <ul>
                        <li>
                          <ElLink href="#mod-system" type="primary" :underline="false">
                            一、系统管理
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-user" type="primary" :underline="false">
                              用户管理
                            </ElLink>
                            ·
                            <ElLink href="#page-role" type="primary" :underline="false">
                              角色管理
                            </ElLink>
                            ·
                            <ElLink href="#page-menu" type="primary" :underline="false">
                              菜单管理
                            </ElLink>
                            ·
                            <ElLink href="#page-dept" type="primary" :underline="false">
                              部门管理
                            </ElLink>
                            ·
                            <ElLink href="#page-position" type="primary" :underline="false">
                              岗位管理
                            </ElLink>
                            ·
                            <ElLink href="#page-dict" type="primary" :underline="false">
                              字典管理
                            </ElLink>
                            ·
                            <ElLink href="#page-param" type="primary" :underline="false">
                              参数配置
                            </ElLink>
                            ·
                            <ElLink href="#page-notice" type="primary" :underline="false">
                              通知公告
                            </ElLink>
                            ·
                            <ElLink href="#page-tenant" type="primary" :underline="false">
                              租户管理
                            </ElLink>
                            ·
                            <ElLink href="#page-log" type="primary" :underline="false">
                              操作日志
                            </ElLink>
                            ·
                            <ElLink href="#page-login" type="primary" :underline="false">
                              登录页
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-monitor" type="primary" :underline="false">
                            二、监控管理
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-online" type="primary" :underline="false">
                              在线用户
                            </ElLink>
                            ·
                            <ElLink href="#page-cache" type="primary" :underline="false">
                              缓存管理
                            </ElLink>
                            ·
                            <ElLink href="#page-resource" type="primary" :underline="false">
                              文件管理
                            </ElLink>
                            ·
                            <ElLink href="#page-server" type="primary" :underline="false">
                              服务监控
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-task" type="primary" :underline="false">
                            三、任务管理
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-cronjob" type="primary" :underline="false">
                              调度器监控
                            </ElLink>
                            ·
                            <ElLink href="#page-cronnode" type="primary" :underline="false">
                              节点管理
                            </ElLink>
                            ·
                            <ElLink href="#page-workflow" type="primary" :underline="false">
                              流程编排
                            </ElLink>
                            ·
                            <ElLink href="#page-nodetype" type="primary" :underline="false">
                              编排节点类型
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-ai" type="primary" :underline="false">
                            四、AI 模块
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-ai-chat" type="primary" :underline="false">
                              AI智能助手
                            </ElLink>
                            ·
                            <ElLink href="#page-ai-fachat" type="primary" :underline="false">
                              会话聊天
                            </ElLink>
                            ·
                            <ElLink href="#page-ai-memory" type="primary" :underline="false">
                              会话记忆
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-generator" type="primary" :underline="false">
                            五、代码生成器
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-gencode" type="primary" :underline="false">
                              代码生成
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-app" type="primary" :underline="false">
                            六、应用管理
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-portal" type="primary" :underline="false">
                              插件市场
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-example" type="primary" :underline="false">
                            七、示例模块
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-demo" type="primary" :underline="false">
                              示例管理
                            </ElLink>
                            ·
                            <ElLink href="#page-demo01" type="primary" :underline="false">
                              三级菜单
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-dashboard" type="primary" :underline="false">
                            八、仪表盘
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-home" type="primary" :underline="false">
                              首页
                            </ElLink>
                            ·
                            <ElLink href="#page-profile" type="primary" :underline="false">
                              个人中心
                            </ElLink>
                            ·
                            <ElLink href="#page-changelog" type="primary" :underline="false">
                              更新日志
                            </ElLink>
                            ·
                            <ElLink href="#page-db-workplace" type="primary" :underline="false">
                              工作台
                            </ElLink>
                            ·
                            <ElLink href="#page-db-console" type="primary" :underline="false">
                              控制台
                            </ElLink>
                            ·
                            <ElLink href="#page-db-analysis" type="primary" :underline="false">
                              分析页
                            </ElLink>
                            ·
                            <ElLink href="#page-db-ecommerce" type="primary" :underline="false">
                              电子商务
                            </ElLink>
                            ·
                            <ElLink href="#page-db-map" type="primary" :underline="false">
                              地图
                            </ElLink>
                            ·
                            <ElLink href="#page-db-pricing" type="primary" :underline="false">
                              定价
                            </ElLink>
                            ·
                            <ElLink href="#page-db-article" type="primary" :underline="false">
                              文章管理
                            </ElLink>
                            ·
                            <ElLink href="#page-db-tutorial" type="primary" :underline="false">
                              教程
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-layout" type="primary" :underline="false">
                            九、布局与通用功能
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#layout-main" type="primary" :underline="false">
                              主布局
                            </ElLink>
                            ·
                            <ElLink href="#layout-sidebar" type="primary" :underline="false">
                              侧栏菜单
                            </ElLink>
                            ·
                            <ElLink href="#layout-header" type="primary" :underline="false">
                              顶栏
                            </ElLink>
                            ·
                            <ElLink href="#layout-worktab" type="primary" :underline="false">
                              标签页
                            </ElLink>
                            ·
                            <ElLink href="#layout-settings" type="primary" :underline="false">
                              设置面板
                            </ElLink>
                            ·
                            <ElLink href="#layout-notification" type="primary" :underline="false">
                              通知
                            </ElLink>
                            ·
                            <ElLink href="#layout-search" type="primary" :underline="false">
                              全局搜索
                            </ElLink>
                            ·
                            <ElLink href="#layout-lock" type="primary" :underline="false">
                              锁屏
                            </ElLink>
                            ·
                            <ElLink href="#layout-user" type="primary" :underline="false">
                              用户菜单
                            </ElLink>
                            ·
                            <ElLink href="#layout-theme" type="primary" :underline="false">
                              主题切换
                            </ElLink>
                            ·
                            <ElLink href="#layout-lang" type="primary" :underline="false">
                              语言切换
                            </ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-exception" type="primary" :underline="false">
                            十、异常页
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-401" type="primary" :underline="false">401</ElLink>
                            ·
                            <ElLink href="#page-403" type="primary" :underline="false">403</ElLink>
                            ·
                            <ElLink href="#page-404" type="primary" :underline="false">404</ElLink>
                            ·
                            <ElLink href="#page-500" type="primary" :underline="false">500</ElLink>
                          </div>
                        </li>
                        <li>
                          <ElLink href="#mod-swagger" type="primary" :underline="false">
                            十一、接口文档（API）
                          </ElLink>
                          <div class="toc-l2">
                            <ElLink href="#page-swagger" type="primary" :underline="false">
                              Swagger文档
                            </ElLink>
                            ·
                            <ElLink href="#page-redoc" type="primary" :underline="false">
                              Redoc文档
                            </ElLink>
                            ·
                            <ElLink href="#page-ljdoc" type="primary" :underline="false">
                              LangJin文档
                            </ElLink>
                          </div>
                        </li>
                      </ul>
                    </ElCard>

                    <!-- 一、系统管理 -->
                    <div class="module" id="mod-system">
                      <h2>
                        一、系统管理
                        <ElTag type="primary" effect="dark" size="small" class="shrink-0">
                          module_system
                        </ElTag>
                      </h2>

                      <!-- 用户管理 -->
                      <div class="page" id="page-user">
                        <h3>
                          1.1 用户管理
                          <ElText tag="span" size="small" type="info" class="path font-mono">
                            module_system/user/index.vue
                          </ElText>
                        </h3>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">API 权限标识</ElDivider>
                          <p>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              module_system:user
                            </ElTag>
                            — 含
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              create
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              delete
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              update
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              detail
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              import
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              export
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              patch
                            </ElTag>
                          </p>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">
                            🔍 搜索/筛选表单（5字段）
                          </ElDivider>
                          <ElCard shadow="never" class="mb-3 overflow-x-auto">
                            <table class="manual-doc-table w-full border-collapse text-sm">
                              <thead>
                                <tr><th>备注</th></tr>
                              </thead>
                              <tbody>
                                <tr><td>文本·账号</td></tr>
                                <tr><td>文本·用户名</td></tr>
                                <tr><td>下拉·启用/停用</td></tr>
                                <tr><td>创建人（UserTableSelect 弹窗选用户）</td></tr>
                                <tr><td>创建时间·日期时间范围</td></tr>
                              </tbody>
                            </table>
                          </ElCard>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">📊 表格列</ElDivider>
                          <ElCard shadow="never" class="mb-3 overflow-x-auto">
                            <table class="manual-doc-table w-full border-collapse text-sm">
                              <thead>
                                <tr><th>渲染</th></tr>
                              </thead>
                              <tbody>
                                <tr><td>固定左侧</td></tr>
                                <tr><td>ElAvatar</td></tr>
                                <tr><td>溢出省略</td></tr>
                                <tr><td>溢出省略</td></tr>
                                <tr>
                                  <td>
                                    <span class="tag tag-success">启用</span>
                                    <span class="tag tag-danger">停用</span>
                                  </td>
                                </tr>
                                <tr><td>row.dept?.name</td></tr>
                                <tr>
                                  <td>
                                    <span class="tag tag-success">男</span>
                                    <span class="tag tag-warning">女</span>
                                    <span class="tag tag-info">未知</span>
                                  </td>
                                </tr>
                                <tr><td></td></tr>
                                <tr><td></td></tr>
                                <tr><td>固定右侧</td></tr>
                              </tbody>
                            </table>
                          </ElCard>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">🔘 工具栏按钮</ElDivider>
                          <ElSpace wrap size="small" class="mb-2">
                            <ElButton type="primary" size="small" plain class="manual-doc-btn">
                              新增
                            </ElButton>
                            <ElButton type="success" size="small" plain class="manual-doc-btn">
                              导入
                            </ElButton>
                            <ElButton type="warning" size="small" plain class="manual-doc-btn">
                              导出
                            </ElButton>
                            <ElButton type="danger" size="small" plain class="manual-doc-btn">
                              删除
                            </ElButton>
                            <ElButton type="info" size="small" plain class="manual-doc-btn">
                              更多(批量启/停用)
                            </ElButton>
                            <ElButton size="small" plain class="manual-doc-btn">刷新</ElButton>
                            <ElButton size="small" plain class="manual-doc-btn">列配置</ElButton>
                          </ElSpace>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">🔘 行操作按钮</ElDivider>
                          <ElSpace wrap size="small" class="mb-2">
                            <ElButton type="warning" size="small" plain class="manual-doc-btn">
                              重置密码
                            </ElButton>
                            <ElButton type="info" size="small" plain class="manual-doc-btn">
                              详情
                            </ElButton>
                            <ElButton type="primary" size="small" plain class="manual-doc-btn">
                              编辑
                            </ElButton>
                            <ElButton type="danger" size="small" plain class="manual-doc-btn">
                              删除
                            </ElButton>
                          </ElSpace>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">📋 弹窗/抽屉</ElDivider>
                          <ul class="feature-list">
                            <li>
                              <strong>详情 Drawer</strong>
                              —
                              编号、头像、账号、用户名、性别(标签)、部门、角色(逗号拼接)、岗位(逗号拼接)、邮箱、手机号、是否超管(标签)、状态(标签)、上次登录时间、创建人、更新人、创建时间、更新时间、描述
                            </li>
                            <li>
                              <strong>新增/编辑 Drawer</strong>
                              (450px) —
                              账号(username,编辑时禁用)、用户名(name)、性别、手机号(正则校验)、邮箱(正则校验)、部门(ElTreeSelect)、角色(多选)、岗位(多选)、密码(仅新增)、是否超管(Switch)、状态(Radio)、描述(textarea)
                            </li>
                            <li>
                              <strong>导入弹窗</strong>
                              — ArtImportDialog, 模板 user_import_template.xlsx
                            </li>
                            <li>
                              <strong>导出弹窗</strong>
                              — FaExportDialog
                            </li>
                            <li>
                              <strong>重置密码弹窗</strong>
                              — 输入新密码, 至少6位
                            </li>
                          </ul>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">✨ 特殊功能</ElDivider>
                          <ul class="feature-list">
                            <li>左侧部门树联动筛选(点击树节点过滤列表)</li>
                            <li>批量删除(确认对话框)</li>
                            <li>批量启用/停用</li>
                            <li>若删除自己则清除登录信息登出</li>
                          </ul>
                        </div>
                      </div>

                      <!-- 角色管理 -->
                      <div class="page" id="page-role">
                        <h3>
                          1.2 角色管理
                          <ElText tag="span" size="small" type="info" class="path font-mono">
                            module_system/role/index.vue
                          </ElText>
                        </h3>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">API 权限标识</ElDivider>
                          <p>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              module_system:role
                            </ElTag>
                            — 含
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              create
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              delete
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              update
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              detail
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              export
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              patch
                            </ElTag>
                            <ElTag effect="plain" type="info" size="small" class="mr-1 font-mono">
                              permission
                            </ElTag>
                          </p>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">
                            🔍 搜索表单（3字段）
                          </ElDivider>
                          <ElCard shadow="never" class="mb-3 overflow-x-auto">
                            <table class="manual-doc-table w-full border-collapse text-sm">
                              <thead>
                                <tr><th>类型</th></tr>
                              </thead>
                              <tbody>
                                <tr><td>文本输入</td></tr>
                                <tr><td>下拉(启用/停用, value="true"/"false")</td></tr>
                                <tr><td>日期时间范围</td></tr>
                              </tbody>
                            </table>
                          </ElCard>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">📊 表格列</ElDivider>
                          <ElCard shadow="never" class="mb-3 overflow-x-auto">
                            <table class="manual-doc-table w-full border-collapse text-sm">
                              <thead>
                                <tr><th>渲染</th></tr>
                              </thead>
                              <tbody>
                                <tr><td>固定左侧</td></tr>
                                <tr><td>溢出省略</td></tr>
                                <tr>
                                  <td>
                                    <span class="tag tag-success">启用</span>
                                    <span class="tag tag-danger">停用</span>
                                  </td>
                                </tr>
                                <tr><td>溢出省略</td></tr>
                                <tr><td>固定右侧</td></tr>
                              </tbody>
                            </table>
                          </ElCard>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">🔘 工具栏按钮</ElDivider>
                          <ElSpace wrap size="small" class="mb-2">
                            <ElButton type="primary" size="small" plain class="manual-doc-btn">
                              新增
                            </ElButton>
                            <ElButton type="warning" size="small" plain class="manual-doc-btn">
                              导出
                            </ElButton>
                            <ElButton type="danger" size="small" plain class="manual-doc-btn">
                              删除
                            </ElButton>
                            <ElButton size="small" plain class="manual-doc-btn">刷新</ElButton>
                            <ElButton size="small" plain class="manual-doc-btn">列配置</ElButton>
                          </ElSpace>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">🔘 行操作按钮</ElDivider>
                          <ElSpace wrap size="small" class="mb-2">
                            <ElButton type="info" size="small" plain class="manual-doc-btn">
                              权限
                            </ElButton>
                            <ElButton type="primary" size="small" plain class="manual-doc-btn">
                              编辑
                            </ElButton>
                            <ElButton type="danger" size="small" plain class="manual-doc-btn">
                              删除
                            </ElButton>
                          </ElSpace>
                        </div>

                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">📋 弹窗/抽屉</ElDivider>
                          <ul class="feature-list">
                            <li>
                              <strong>新增/编辑 Drawer</strong>
                              (450px) — 名称、标识(编辑时禁用)、排序、状态(Radio)、权限树(ElTree,
                              勾选)、备注(textarea)
                            </li>
                            <li>
                              <strong>权限 Drawer</strong>
                              (600px) — 权限菜单树(ElTree, 勾选, 支持展开/收起)
                            </li>
                            <li>
                              <strong>导出弹窗</strong>
                              — FaExportDialog
                            </li>
                          </ul>
                        </div>
                      </div>

                      <!-- 系统管理：其余页面（完整性验收要点，与实现对齐便于漏项检查） -->
                      <div
                        v-for="p in manualSystemTailPages"
                        :key="p.anchor"
                        class="page"
                        :id="p.anchor"
                      >
                        <h3>
                          {{ p.title }}
                          <ElText tag="span" size="small" type="info" class="path font-mono">
                            {{ p.path }}
                          </ElText>
                        </h3>
                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">
                            功能完整性验收
                          </ElDivider>
                          <ul class="feature-list">
                            <li v-for="(line, idx) in p.notes" :key="idx">{{ line }}</li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <!-- 二～十一：其余业务模块 -->
                    <div
                      v-for="mod in manualModulesAfterSystem"
                      :key="mod.anchor"
                      class="module"
                      :id="mod.anchor"
                    >
                      <h2>
                        {{ mod.heading }}
                        <ElTag
                          v-if="mod.pkgTag"
                          type="primary"
                          effect="dark"
                          size="small"
                          class="shrink-0"
                        >
                          {{ mod.pkgTag }}
                        </ElTag>
                      </h2>
                      <div v-for="p in mod.pages" :key="p.anchor" class="page" :id="p.anchor">
                        <h3>
                          {{ p.title }}
                          <ElText tag="span" size="small" type="info" class="path font-mono">
                            {{ p.path }}
                          </ElText>
                        </h3>
                        <div class="section">
                          <ElDivider content-position="left" class="!my-3">
                            功能完整性验收
                          </ElDivider>
                          <ul class="feature-list">
                            <li v-for="(line, idx) in p.notes" :key="idx">{{ line }}</li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div
                      class="manual-footer-note mt-10 border-t border-g-200 pt-6 text-center text-xs text-g-500 dark:border-g-700 dark:text-g-400"
                    >
                      <p>
                        FastapiAdmin 功能点清单（完整性）—
                        与当前代码中已实现界面项对齐，用于逐项核对是否漏测，不评价体验优劣。
                      </p>
                    </div>
                  </div>
                </div>
              </ElScrollbar>
            </div>
          </div>
        </ElTabPane>
      </ElTabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import lockImg from "@imgs/lock/bg_dark.webp";

defineOptions({ name: "DashboardTutorial" });

/** 演示用在线 MP4，上线后建议改为自有 OSS / 静态资源地址 */
const DEFAULT_VIDEO =
  "//lf3-static.bytednsdoc.com/obj/eden-cn/nupenuvpxnuvo/xgplayer_doc/xgplayer-demo.mp4";

const videoUrl = ref(DEFAULT_VIDEO);
const posterUrl = ref(lockImg);
</script>

<style scoped lang="scss">
.tutorial-page__player {
  width: 100%;
  max-height: min(78vh, 880px);
  padding: 10px 12px;
  overflow: auto;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--el-border-radius-base);

  &--empty {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 120px;
  }

  &__module + &__module {
    padding-top: 12px;
    margin-top: 12px;
    border-top: 1px solid var(--el-border-color-lighter);
  }

  &__mod-title {
    display: block;
    width: 100%;
    padding: 4px 0;
    margin: 0;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.4;
    color: var(--el-color-primary);
    text-align: left;
    cursor: pointer;
    background: transparent;
    border: none;

    &:hover {
      text-decoration: underline;
    }
  }

  &__pages {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding-left: 4px;
    margin-top: 6px;
  }

  &__page {
    display: block;
    width: 100%;
    padding: 3px 6px;
    margin: 0;
    font-size: 12px;
    line-height: 1.35;
    color: var(--el-text-color-regular);
    text-align: left;
    cursor: pointer;
    background: transparent;
    border: none;
    border-radius: 4px;

    &:hover {
      color: var(--el-color-primary);
      background: var(--el-fill-color-light);
    }
  }
}

/* 手册正文（避免使用全局类名 container；补齐排版与表格样式） */
.manual-html {
  padding: 16px 18px 28px;
  font-size: 14px;
  line-height: 1.65;
  color: var(--el-text-color-primary);

  &__inner {
    max-width: 100%;
  }

  h1 {
    margin: 0 0 1rem;
    font-size: 1.375rem;
    font-weight: 600;

    small {
      display: block;
      margin-top: 0.4rem;
      font-size: 0.8125rem;
      font-weight: normal;
      line-height: 1.5;
      color: var(--el-text-color-secondary);
    }
  }

  .toc ul {
    padding: 0;
    margin: 0;
    list-style: none;
  }

  .toc li {
    margin-bottom: 0.85rem;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .toc-l2 {
    margin-top: 0.4rem;
    line-height: 1.85;
    word-break: break-all;
    overflow-wrap: anywhere;
  }

  .module {
    padding-top: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid var(--el-border-color-lighter);
  }

  /* 紧跟目录卡片后的首个业务模块（前面还有 h1 + ElCard，不能用 :first-of-type） */
  .toc + .module {
    padding-top: 0;
    margin-top: 1.25rem;
    border-top: none;
  }

  .module h2 {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    margin: 0 0 1rem;
    font-size: 1.125rem;
    font-weight: 600;
  }

  .page {
    padding-bottom: 1.25rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px dashed var(--el-border-color-light);

    &:last-child {
      padding-bottom: 0;
      margin-bottom: 0;
      border-bottom: none;
    }
  }

  .page h3 {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: baseline;
    margin: 0 0 0.75rem;
    font-size: 1.0625rem;
    font-weight: 600;

    .path {
      font-weight: normal;
    }
  }

  .section {
    margin-bottom: 0.65rem;
  }

  .feature-list {
    padding-left: 1.2rem;
    margin: 0.35rem 0 0;

    li {
      margin-bottom: 0.4rem;
    }
  }

  .manual-doc-table {
    th,
    td {
      padding: 6px 10px;
      border: 1px solid var(--el-border-color-lighter);
    }

    th {
      font-weight: 500;
      text-align: left;
      background: var(--el-fill-color-light);
    }
  }

  /* 文档内按钮仅为示意，避免误点触发业务样式反馈 */
  .manual-doc-btn {
    pointer-events: none;
  }

  .tag {
    display: inline-block;
    padding: 2px 8px;
    font-size: 12px;
    line-height: 1.4;
    border-radius: 4px;

    &.tag-success {
      color: var(--el-color-success);
      background: var(--el-color-success-light-9);
    }

    &.tag-danger {
      color: var(--el-color-danger);
      background: var(--el-color-danger-light-9);
    }

    &.tag-warning {
      color: var(--el-color-warning);
      background: var(--el-color-warning-light-9);
    }

    &.tag-info {
      color: var(--el-color-info);
      background: var(--el-color-info-light-9);
    }
  }

  .manual-footer-note {
    clear: both;
  }
}

// 响应式适配
@media (width <= 960px) {
  .manual-feature-body__layout {
    grid-template-columns: 1fr;
  }

  .manual-feature-body__aside {
    width: 100%;
    min-width: 0;
    max-width: none;
  }

  .manual-nav {
    max-height: 40vh;
  }

  .manual-html {
    padding: 12px 12px 24px;
  }
}
</style>
