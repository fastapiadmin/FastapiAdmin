<!-- 文章详情（抽屉，无独立路由） -->
<template>
  <ElDrawer
    v-model="visible"
    :title="drawerTitle"
    direction="rtl"
    size="min(900px, 100vw)"
    destroy-on-close
    append-to-body
    class="article-detail-drawer"
  >
    <div v-loading="loading" class="article-detail-drawer-inner">
      <ElAlert v-if="error" :title="error" type="error" show-icon :closable="false" />
      <div
        v-else-if="articleHtml"
        class="markdown-body article-detail-markdown"
        v-highlight
        v-html="articleHtml"
      />
    </div>
    <template #footer>
      <div class="flex flex-wrap justify-end gap-2">
        <ElButton v-if="articleId != null" @click="emitOpenCommentWall">
          <FaSvgIcon icon="ri:message-3-line" class="mr-1" />
          留言讨论
        </ElButton>
        <ElButton @click="visible = false">关闭</ElButton>
        <ElButton v-if="articleId != null" v-auth="'edit'" type="primary" @click="onEditClick">
          编辑
        </ElButton>
      </div>
    </template>
  </ElDrawer>
</template>

<script setup lang="ts">
import "@styles/core/md.scss";
import "@styles/custom/one-dark-pro.scss";
import axios from "axios";

defineOptions({ name: "ArticleDetailDrawer" });

const props = defineProps<{
  modelValue: boolean;
  articleId?: number | null;
}>();

const emit = defineEmits<{
  "update:modelValue": [boolean];
  edit: [id: number];
  "open-comment-wall": [];
}>();

const emitOpenCommentWall = () => {
  emit("open-comment-wall");
};

const visible = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit("update:modelValue", v),
});

interface ArticleResponse {
  code: number;
  data: {
    title: string;
    html_content: string;
  };
}

const articleTitle = ref("");
const articleHtml = shallowRef("");
const loading = ref(false);
const error = ref<string | null>(null);

const drawerTitle = computed(() => articleTitle.value || "文章详情");

const fetchDetail = async () => {
  const id = props.articleId;
  if (id == null) return;

  loading.value = true;
  error.value = null;
  articleTitle.value = "";
  articleHtml.value = "";

  try {
    const { data } = await axios.get<ArticleResponse>(
      "https://www.qiniu.lingchen.kim/blog_detail.json"
    );

    if (data.code === 200) {
      articleTitle.value = data.data.title;
      articleHtml.value = data.data.html_content;
    } else {
      error.value = "文章加载失败";
    }
  } catch (err) {
    error.value = "文章加载失败";
    console.error("获取文章详情失败:", err);
  } finally {
    loading.value = false;
  }
};

const onEditClick = () => {
  if (props.articleId != null) {
    emit("edit", props.articleId);
  }
};

watch(
  () => [props.modelValue, props.articleId] as const,
  ([open, id]) => {
    if (open && id != null) {
      nextTick(() => fetchDetail());
    }
  }
);
</script>

<style lang="scss" scoped>
.article-detail-drawer-inner {
  min-height: 120px;
}

.article-detail-markdown {
  margin-top: 8px;

  ::deep(img) {
    width: 100%;
    border: 1px solid var(--fa-gray-200);
  }

  ::deep(pre) {
    position: relative;

    &:hover {
      .copy-button {
        opacity: 1;
      }
    }

    &::before {
      position: absolute;
      top: 0;
      left: 50px;
      width: 1px;
      height: 100%;
      content: "";
      background: #0a0a0e;
    }
  }

  ::deep(.code-wrapper) {
    overflow-x: auto;
  }

  ::deep(.line-number) {
    position: sticky;
    left: 0;
    z-index: 2;
    box-sizing: border-box;
    display: inline-block;
    width: 50px;
    margin-right: 10px;
    font-size: 14px;
    color: #9e9e9e;
    text-align: center;
  }

  ::deep(.copy-button) {
    position: absolute;
    top: 6px;
    right: 6px;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    font-size: 20px;
    line-height: 40px;
    color: #999;
    text-align: center;
    cursor: pointer;
    background-color: #000;
    border: none;
    border-radius: 8px;
    opacity: 0;
    transition: all 0.2s;
  }
}
</style>
