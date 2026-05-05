declare module "vue3-cron-plus" {
  import { DefineComponent } from "vue";

  export const vue3CronPlus: DefineComponent<{}, {}, any>;

  export default vue3CronPlus;
}

declare module "vue3-cron-plus/dist/index.css" {
  const content: any;
  export default content;
}
