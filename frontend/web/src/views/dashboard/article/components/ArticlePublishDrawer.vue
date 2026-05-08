<!-- 文章新增 / 编辑（抽屉，替代独立发布页） -->
<template>
  <ElDrawer
    v-model="visible"
    :title="drawerTitle"
    direction="rtl"
    size="min(920px, 100vw)"
    destroy-on-close
    append-to-body
    class="article-publish-drawer"
  >
    <div class="article-publish-drawer-body">
      <template v-if="resultPhase === 'form'">
        <div>
          <ElRow :gutter="10">
            <ElCol :span="18">
              <ElInput
                v-model.trim="articleName"
                placeholder="请输入文章标题（最多100个字符）"
                maxlength="100"
              />
            </ElCol>
            <ElCol :span="6">
              <ElSelect v-model="articleType" placeholder="请选择文章类型" filterable>
                <ElOption
                  v-for="item in articleTypes"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </ElSelect>
            </ElCol>
          </ElRow>

          <ArtWangEditor class="mt-2.5" v-model="editorHtml" />

          <div class="p-5 mt-5 art-card-xs">
            <h2 class="mb-5 text-xl font-medium">发布设置</h2>
            <ElForm>
              <ElFormItem label="封面">
                <div class="mt-2.5">
                  <ElUpload
                    :action="uploadImageUrl"
                    :headers="uploadHeaders"
                    :show-file-list="false"
                    :on-success="onSuccess"
                    :on-error="onError"
                    :before-upload="beforeUpload"
                  >
                    <div
                      v-if="!cover"
                      class="flex-cc flex-col w-65 h-40 border border-dashed border-[#d9d9d9] rounded-md"
                    >
                      <ElIcon class="!text-xl !text-g-600"><Plus /></ElIcon>
                      <div class="mt-2 text-sm text-g-600">点击上传封面</div>
                    </div>
                    <img v-else :src="cover" class="block w-65 h-40 object-cover" />
                  </ElUpload>
                  <div class="mt-2 text-xs text-g-700">建议尺寸 16:9，jpg/png 格式</div>
                </div>
              </ElFormItem>
              <ElFormItem label="可见">
                <ElSwitch v-model="visibleFlag" />
              </ElFormItem>
            </ElForm>

            <div class="flex justify-end">
              <ElButton type="primary" @click="submit" class="w-25">
                {{ pageMode === PageModeEnum.Edit ? "保存" : "发布" }}
              </ElButton>
            </div>
          </div>
        </div>
      </template>

      <ArtResultPage
        v-else-if="resultPhase === 'success'"
        type="success"
        :title="successTitle"
        message="文章操作已完成。简单反馈也可用全局 Message；此处用于完整结果反馈，下方灰色区域可展示补充说明。"
        icon-code="ri:check-fill"
      >
        <template #content>
          <p v-if="pageMode === PageModeEnum.Add">文章已发布，读者可在列表与详情中查看。</p>
          <p v-else>修改已保存，内容已更新。</p>
        </template>
        <template #buttons>
          <ElButton type="primary" v-ripple @click="backToForm">继续编辑</ElButton>
          <ElButton v-ripple @click="finishAndClose">关闭并返回列表</ElButton>
          <ElButton v-if="pageMode === PageModeEnum.Add" v-ripple @click="publishAgain">
            新建一篇
          </ElButton>
        </template>
      </ArtResultPage>

      <ArtResultPage
        v-else
        type="fail"
        :title="failTitle"
        message="请核对并修改以下信息后，再重新提交。"
        icon-code="ri:close-fill"
      >
        <template #content>
          <p>本次提交未成功，可能原因如下：</p>
          <p>
            <ArtSvgIcon icon="ri:close-circle-line" class="text-red-500 mr-1" />
            <span>网络或服务暂时不可用，请稍后重试</span>
          </p>
          <p>
            <ArtSvgIcon icon="ri:close-circle-line" class="text-red-500 mr-1" />
            <span>请确认必填项与封面已正确填写</span>
          </p>
        </template>
        <template #buttons>
          <ElButton type="primary" v-ripple @click="backToForm">返回修改</ElButton>
          <ElButton v-ripple @click="finishAndClose">关闭并返回列表</ElButton>
        </template>
      </ArtResultPage>
    </div>
  </ElDrawer>
</template>

<script setup lang="ts">
import { Plus } from "@element-plus/icons-vue";
import { ApiStatus } from "@utils/http";
import { useUserStore } from "@stores/modules/user.store";
import { EmojiText } from "@utils/ui";
import { PageModeEnum } from "@/enums/formEnum";
import axios from "axios";

defineOptions({ name: "ArticlePublishDrawer" });

const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    /** 编辑的文章 id；不传或 null 为新增 */
    editId?: number | null;
  }>(),
  { editId: null }
);

const emit = defineEmits<{
  "update:modelValue": [boolean];
  success: [];
}>();

const visible = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit("update:modelValue", v),
});

interface ArticleType {
  id: number;
  name: string;
}

interface UploadResponse {
  data: {
    url: string;
  };
}

interface ArticleDetailResponse {
  code: number;
  data: {
    title: string;
    blog_class: string;
    html_content: string;
  };
}

const MAX_IMAGE_SIZE = 2;
const EMPTY_EDITOR_CONTENT = "<p><br></p>";

const userStore = useUserStore();
const { accessToken } = userStore;

const uploadImageUrl = `${import.meta.env.VITE_API_URL}/api/common/upload`;
const uploadHeaders = { Authorization: accessToken };

type ResultPhase = "form" | "success" | "fail";
const resultPhase = ref<ResultPhase>("form");

const pageMode = ref<PageModeEnum>(PageModeEnum.Add);
const articleName = ref("");
const articleType = ref<number>();
const articleTypes = ref<ArticleType[]>([]);
const editorHtml = ref("");
const cover = ref("");
/** 与 ElSwitch `visible` 避免命名冲突 */
const visibleFlag = ref(true);

const drawerTitle = computed(() =>
  pageMode.value === PageModeEnum.Edit ? "编辑文章" : "新增文章"
);

const successTitle = computed(() =>
  pageMode.value === PageModeEnum.Edit ? "保存成功" : "发布成功"
);
const failTitle = computed(() => (pageMode.value === PageModeEnum.Edit ? "保存失败" : "发布失败"));

const backToForm = () => {
  resultPhase.value = "form";
};

const finishAndClose = () => {
  emit("success");
  visible.value = false;
};

const publishAgain = () => {
  pageMode.value = PageModeEnum.Add;
  articleName.value = "";
  articleType.value = undefined;
  editorHtml.value = "";
  cover.value = "";
  visibleFlag.value = true;
  resultPhase.value = "form";
};

const initWhenOpen = () => {
  resultPhase.value = "form";
  pageMode.value = props.editId != null ? PageModeEnum.Edit : PageModeEnum.Add;

  if (pageMode.value === PageModeEnum.Edit) {
    getArticleDetail();
  } else {
    articleName.value = "";
    articleType.value = undefined;
    editorHtml.value = "";
    cover.value = "";
    visibleFlag.value = true;
  }
};

const getArticleTypes = async () => {
  try {
    const { data } = await axios.get("https://www.qiniu.lingchen.kim/classify.json");
    if (data.code === 200) {
      articleTypes.value = data.data;
    }
  } catch (error) {
    console.error("获取文章分类失败:", error);
    ElMessage.error("获取文章分类失败");
  }
};

const getArticleDetail = async () => {
  try {
    const { data } = await axios.get<ArticleDetailResponse>(
      "https://www.qiniu.lingchen.kim/blog_list.json"
    );

    if (data.code === ApiStatus.success) {
      const { title, blog_class, html_content } = data.data;
      articleName.value = title;
      articleType.value = Number(blog_class);
      editorHtml.value = html_content;
    }
  } catch (error) {
    console.error("获取文章详情失败:", error);
    ElMessage.error("获取文章详情失败");
  }
};

const validateArticle = (): boolean => {
  if (!articleName.value.trim()) {
    ElMessage.error("请输入文章标题");
    return false;
  }

  if (!articleType.value) {
    ElMessage.error("请选择文章类型");
    return false;
  }

  if (!editorHtml.value || editorHtml.value === EMPTY_EDITOR_CONTENT) {
    ElMessage.error("请输入文章内容");
    return false;
  }

  if (!cover.value) {
    ElMessage.error("请上传封面图片");
    return false;
  }

  return true;
};

const cleanCodeContent = (content: string): string => {
  return content.replace(/(\s*)<\/code>/g, "</code>");
};

const addArticle = async () => {
  if (!validateArticle()) return;

  try {
    const cleanedContent = cleanCodeContent(editorHtml.value);

    console.log("新增文章:", { cleanedContent });

    await new Promise<void>((resolve) => setTimeout(resolve, 400));
    resultPhase.value = "success";
  } catch (error) {
    console.error("发布文章失败:", error);
    resultPhase.value = "fail";
  }
};

const editArticle = async () => {
  if (!validateArticle()) return;

  try {
    const cleanedContent = cleanCodeContent(editorHtml.value);

    console.log("编辑文章:", { cleanedContent });

    await new Promise<void>((resolve) => setTimeout(resolve, 400));
    resultPhase.value = "success";
  } catch (error) {
    console.error("保存文章失败:", error);
    resultPhase.value = "fail";
  }
};

const submit = () => {
  if (pageMode.value === PageModeEnum.Edit) {
    editArticle();
  } else {
    addArticle();
  }
};

const onSuccess = (response: UploadResponse) => {
  cover.value = response.data.url;
  ElMessage.success(`图片上传成功 ${EmojiText[200]}`);
};

const onError = () => {
  ElMessage.error(`图片上传失败 ${EmojiText[500]}`);
};

const beforeUpload = (file: File): boolean => {
  const isImage = file.type.startsWith("image/");
  const isLt2M = file.size / 1024 / 1024 < MAX_IMAGE_SIZE;

  if (!isImage) {
    ElMessage.error("只能上传图片文件");
    return false;
  }

  if (!isLt2M) {
    ElMessage.error(`图片大小不能超过 ${MAX_IMAGE_SIZE}MB`);
    return false;
  }

  return true;
};

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      nextTick(() => {
        initWhenOpen();
        getArticleTypes();
      });
    }
  }
);
</script>

<style scoped lang="scss">
.article-publish-drawer-body {
  padding-bottom: env(safe-area-inset-bottom, 0);
}
</style>
