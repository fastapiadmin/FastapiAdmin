<template>
  <div class="fa-card p-5 h-112">
    <div class="fa-card-header">
      <div class="title">
        <h4>年度销售额</h4>
        <p>按季度统计</p>
      </div>
    </div>

    <FaBarChart
      :showAxisLabel="false"
      :showAxisLine="false"
      :showSplitLine="false"
      :data="[50, 80, 50, 90, 60, 70, 50]"
      barWidth="26px"
      height="calc(100% - 155px)"
    />
    <div class="flex justify-around mt-10">
      <div class="flex items-center">
        <div
          class="flex items-center justify-center size-10.5 mr-2.5 text-theme bg-theme/10 rounded-lg"
        >
          <FaSvgIcon icon="ri:money-cny-circle-line" class="text-xl" />
        </div>
        <div>
          <p class="text-lg">¥200,858</p>
          <span class="text-sm">线上销售</span>
        </div>
      </div>
      <div class="flex items-center">
        <div
          class="flex items-center justify-center size-10.5 mr-2.5 text-theme bg-theme/10 rounded-lg"
        >
          <FaSvgIcon icon="ri:heart-3-line" class="text-xl" />
        </div>
        <div>
          <p class="text-lg">¥102,927</p>
          <span class="text-sm">线下销售</span>
        </div>
      </div>
    </div>
  </div>
</template>
