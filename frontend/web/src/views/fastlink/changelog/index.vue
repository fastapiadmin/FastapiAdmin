<!-- 项目版本更新日志（API） -->
<template>
  <div class="mx-auto pt-5 mb-5">
    <h3 class="text-2xl font-medium text-g-900 mb-8">{{ $t("menus.changelog.title") }}</h3>

    <div v-loading="loading" class="space-y-5">
      <div
        v-for="item in upgradeLogList"
        :key="item.version"
        class="fa-card-sm rounded-lg p-6 transition-shadow max-md:p-4"
      >
        <div class="flex items-center justify-between gap-3 mb-4 flex-wrap">
          <span class="px-3 py-1 bg-theme/10 text-theme text-sm font-medium rounded-full">
            {{ item.version }}
          </span>
          <span class="text-sm text-g-500">{{ item.date }}</span>
        </div>

        <h4 class="text-lg font-medium text-g-900 mb-3">{{ item.title }}</h4>

        <pre
          v-if="item.content"
          class="text-sm text-g-700 whitespace-pre-wrap font-sans leading-relaxed mb-4"
          >{{ item.content }}</pre
        >

        <div v-if="item.description" class="text-sm text-g-800 bg-g-300/60 rounded p-3 mb-3">
          {{ item.description }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import VersionAPI from "@/api/module_system/version";

defineOptions({ name: "SystemChangeLog" });

interface UpgradeLog {
  version: string;
  title: string;
  date: string | null;
  content?: string | null;
  description?: string | null;
}

const upgradeLogList = ref<UpgradeLog[]>([]);
const loading = ref(false);

const fetchData = async () => {
  loading.value = true;
  try {
    const { data: res } = await VersionAPI.getPublishedVersions();
    if (res?.data) {
      upgradeLogList.value = res.data.map((item: any) => ({
        version: item.version,
        title: item.title,
        date: item.date,
        content: item.content || null,
        description: item.description,
      }));
    }
  } catch {
    // silently fail
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>
