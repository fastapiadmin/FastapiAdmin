<template>
  <div class="fa-card p-5 pt-3.5 h-46">
    <div class="fa-card-header">
      <div class="title">
        <h4 class="text-2xl">
          <span>14.5k</span>
          <FaSvgIcon icon="ri:arrow-right-up-line" class="text-success text-lg ml-1" />
        </h4>
        <p>销售量</p>
      </div>
    </div>

    <FaBarChart
      :showAxisLabel="false"
      :showAxisLine="false"
      :showSplitLine="false"
      :data="[50, 80, 50, 90, 60, 70, 50]"
      barWidth="16px"
      height="5.6rem"
    />
  </div>
</template>
