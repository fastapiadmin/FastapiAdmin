<template>
  <div class="art-card p-5 pt-3.5 mb-5 h-46 max-sm:mb-4">
    <div class="art-card-header">
      <div class="title">
        <h4 class="text-2xl">
          <span>12%</span>
          <ArtSvgIcon icon="ri:arrow-right-up-line" class="text-success text-lg ml-1" />
        </h4>
        <p>增长</p>
      </div>
    </div>

    <ArtLineChart
      :show-area-color="true"
      :show-axis-label="false"
      :show-axis-line="false"
      :show-split-line="false"
      :data="[50, 85, 65, 95, 75, 130, 180]"
      bar-width="16px"
      height="5rem"
    />
  </div>
</template>
