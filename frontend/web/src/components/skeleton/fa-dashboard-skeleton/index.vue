<!--
  FaDashboardSkeleton：仪表盘页面骨架屏。
  提供统计卡片区域 + 图表区域 + 侧边栏的 shimmer 占位。
-->
<template>
  <ElSkeleton animated>
    <template #template>
      <div class="fa-dashboard-skeleton">
        <!-- 横幅 Banner 占位 -->
        <ElSkeletonItem variant="rect" class="sk-banner" />

        <!-- 统计卡片行 -->
        <div class="sk-card-row">
          <div v-for="i in 4" :key="'card' + i" class="sk-card">
            <div class="sk-card__icon">
              <ElSkeletonItem variant="circle" />
            </div>
            <div class="sk-card__body">
              <ElSkeletonItem variant="text" class="sk-h-4" />
              <ElSkeletonItem variant="text" class="sk-h-6 sk-w-2/3" />
              <ElSkeletonItem variant="text" class="sk-h-3 sk-w-1/2" />
            </div>
          </div>
        </div>

        <!-- 主区域：图表 + 侧边栏 -->
        <div class="sk-main">
          <div class="sk-main__left">
            <!-- 图表卡片 -->
            <div class="sk-chart-card">
              <div class="sk-chart-card__header">
                <ElSkeletonItem variant="text" class="sk-h-5 sk-w-1/4" />
                <ElSkeletonItem variant="text" class="sk-h-3 sk-w-1/6" />
              </div>
              <ElSkeletonItem variant="rect" class="sk-chart" />
            </div>
            <!-- 迷你图表行 -->
            <div class="sk-mini-row">
              <div v-for="i in 3" :key="'mini' + i" class="sk-mini-card">
                <ElSkeletonItem variant="text" class="sk-h-4 sk-w-1/2" />
                <ElSkeletonItem variant="text" class="sk-h-7" />
                <ElSkeletonItem variant="rect" class="sk-mini-chart" />
              </div>
            </div>
          </div>
          <div class="sk-main__right">
            <!-- 侧边栏：活动列表 -->
            <div class="sk-list-card">
              <div class="sk-list-card__header">
                <ElSkeletonItem variant="text" class="sk-h-5 sk-w-1/3" />
              </div>
              <div v-for="i in 4" :key="'item' + i" class="sk-list-item">
                <ElSkeletonItem variant="circle" class="sk-avatar" />
                <div class="sk-list-item__body">
                  <ElSkeletonItem variant="text" class="sk-h-4" />
                  <ElSkeletonItem variant="text" class="sk-h-3 sk-w-2/3" />
                </div>
              </div>
            </div>
            <!-- 待办列表 -->
            <div class="sk-todo-card">
              <div class="sk-todo-card__header">
                <ElSkeletonItem variant="text" class="sk-h-5 sk-w-1/4" />
              </div>
              <div v-for="i in 3" :key="'todo' + i" class="sk-todo-item">
                <ElSkeletonItem variant="text" class="sk-h-4 sk-w-3/4" />
                <ElSkeletonItem variant="text" class="sk-h-3 sk-w-1/3" />
              </div>
            </div>
          </div>
        </div>

        <!-- 底部卡片行 -->
        <div class="sk-bottom-row">
          <div v-for="i in 2" :key="'bottom' + i" class="sk-bottom-card">
            <div class="sk-bottom-card__header">
              <ElSkeletonItem variant="text" class="sk-h-5 sk-w-1/4" />
              <ElSkeletonItem variant="text" class="sk-h-3 sk-w-1/6" />
            </div>
            <ElSkeletonItem variant="rect" class="sk-bottom-chart" />
          </div>
        </div>
      </div>
    </template>
  </ElSkeleton>
</template>

<style lang="scss" scoped>
.fa-dashboard-skeleton {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 8px 0;

  /* 通用高度和宽度 */
  .sk-h-3 {
    height: 12px;
  }

  .sk-h-4 {
    height: 16px;
  }

  .sk-h-5 {
    height: 20px;
  }

  .sk-h-6 {
    height: 24px;
  }

  .sk-h-7 {
    height: 28px;
  }

  .sk-w-1\2 {
    width: 50%;
  }

  .sk-w-1\3 {
    width: 33%;
  }

  .sk-w-1\4 {
    width: 25%;
  }

  .sk-w-1\6 {
    width: 16%;
  }

  .sk-w-2\3 {
    width: 66%;
  }

  .sk-w-3\4 {
    width: 75%;
  }

  /* Banner */
  .sk-banner {
    width: 100%;
    height: 180px;
    border-radius: var(--custom-radius, 12px);
  }

  /* 统计卡片行 */
  .sk-card-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;

    .sk-card {
      display: flex;
      gap: 12px;
      padding: 16px;
      background: var(--el-fill-color-lighter);
      border-radius: var(--custom-radius, 12px);

      .el-skeleton__item--circle {
        width: 40px;
        height: 40px;
      }

      .sk-card__body {
        display: flex;
        flex: 1;
        flex-direction: column;
        gap: 8px;
      }
    }
  }

  /* 主区域 - 图表 + 侧边栏 */
  .sk-main {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 20px;

    .sk-main__left {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .sk-main__right {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .sk-chart-card {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      background: var(--el-fill-color-lighter);
      border-radius: var(--custom-radius, 12px);

      .sk-chart-card__header {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .sk-chart {
        width: 100%;
        height: 280px;
        border-radius: 8px;
      }
    }

    .sk-mini-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;

      .sk-mini-card {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 14px;
        background: var(--el-fill-color-lighter);
        border-radius: var(--custom-radius, 12px);

        .sk-mini-chart {
          width: 100%;
          height: 60px;
          border-radius: 6px;
        }
      }
    }

    /* 侧边栏列表 */
    .sk-list-card,
    .sk-todo-card {
      padding: 16px;
      background: var(--el-fill-color-lighter);
      border-radius: var(--custom-radius, 12px);

      .sk-list-card__header,
      .sk-todo-card__header {
        margin-bottom: 12px;
      }
    }

    .sk-list-item {
      display: flex;
      gap: 10px;
      align-items: center;
      padding: 8px 0;

      .sk-avatar {
        flex-shrink: 0;
        width: 32px;
        height: 32px;
      }

      .sk-list-item__body {
        display: flex;
        flex: 1;
        flex-direction: column;
        gap: 6px;
      }
    }

    .sk-todo-item {
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding: 10px 0;
      border-bottom: 1px solid var(--el-border-color-extra-light);
    }
  }

  /* 底部卡片行 */
  .sk-bottom-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;

    .sk-bottom-card {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px;
      background: var(--el-fill-color-lighter);
      border-radius: var(--custom-radius, 12px);

      .sk-bottom-card__header {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .sk-bottom-chart {
        width: 100%;
        height: 180px;
        border-radius: 8px;
      }
    }
  }
}
</style>
