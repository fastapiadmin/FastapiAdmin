<!-- 文章发布（/dashboard/article/publish） -->
<template>
  <div>
    <template v-if="resultPhase === 'form'">
      <div>
        <div class="max-w-250 mx-auto my-5">
          <!-- 文章标题、类型 -->
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

          <!-- 富文本编辑器 -->
          <ArtWangEditor class="mt-2.5" v-model="editorHtml" />

          <div class="p-5 mt-5 art-card-xs">
            <h2 class="mb-5 text-xl font-medium">发布设置</h2>
            <!-- 图片上传 -->
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
                <ElSwitch v-model="visible" />
              </ElFormItem>
            </ElForm>

            <div class="flex justify-end">
              <ElButton type="primary" @click="submit" class="w-25">
                {{ pageMode === PageModeEnum.Edit ? "保存" : "发布" }}
              </ElButton>
            </div>
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
        <ElButton v-ripple @click="goArticleList">查看列表</ElButton>
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
        <ElButton v-ripple @click="goArticleList">查看列表</ElButton>
      </template>
    </ArtResultPage>
  </div>
</template>

<script setup lang="ts">
import { Plus } from "@element-plus/icons-vue";
import { ApiStatus } from "@/utils/http";
import { useUserStore } from "@/store/modules/user.store";
import { EmojiText } from "@/utils/ui";
import { PageModeEnum } from "@/enums/formEnum";
import axios from "axios";
import { useCommon } from "@/hooks/core/useCommon";

defineOptions({ name: "ArticlePublish" });

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

const MAX_IMAGE_SIZE = 2; // MB
const EMPTY_EDITOR_CONTENT = "<p><br></p>";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const { accessToken } = userStore;
const { scrollToTop } = useCommon();

const uploadImageUrl = `${import.meta.env.VITE_API_URL}/api/common/upload`;
const uploadHeaders = { Authorization: accessToken };

type ResultPhase = "form" | "success" | "fail";
const resultPhase = ref<ResultPhase>("form");

const pageMode = ref<PageModeEnum>(PageModeEnum.Add);
const articleName = ref("");
const articleType = ref<number>();
const articleTypes = ref<ArticleType[]>([]);
const editorHtml = ref("");
const createDate = ref("");
const cover = ref("");
const visible = ref(true);

const successTitle = computed(() =>
  pageMode.value === PageModeEnum.Edit ? "保存成功" : "发布成功"
);
const failTitle = computed(() => (pageMode.value === PageModeEnum.Edit ? "保存失败" : "发布失败"));

const backToForm = () => {
  resultPhase.value = "form";
  scrollToTop();
};

const goArticleList = () => {
  router.push({ name: "ArticleList" });
};

/** 清空表单并停留在「新增发布」（与结果页示例中的再次操作类似） */
const publishAgain = async () => {
  await router.replace({ name: "ArticlePublish" });
  pageMode.value = PageModeEnum.Add;
  articleName.value = "";
  articleType.value = undefined;
  editorHtml.value = "";
  cover.value = "";
  visible.value = true;
  createDate.value = formatDate(useNow().value);
  resultPhase.value = "form";
  scrollToTop();
};

/**
 * 初始化页面模式（新增或编辑）
 */
const initPageMode = () => {
  const { id } = route.query;
  pageMode.value = id ? PageModeEnum.Edit : PageModeEnum.Add;

  if (pageMode.value === PageModeEnum.Edit) {
    getArticleDetail();
  } else {
    createDate.value = formatDate(useNow().value);
  }
};

/**
 * 获取文章分类列表
 */
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

  // TODO: 替换为真实 API 调用
  // const res = await ArticleService.getArticleTypes({})
  // if (res.code === ApiStatus.success) {
  //   articleTypes.value = res.data
  // }
};

/**
 * 获取文章详情（编辑模式）
 */
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

/**
 * 格式化日期为 YYYY-MM-DD 格式
 */
const formatDate = (date: string | Date): string => {
  return useDateFormat(date, "YYYY-MM-DD").value;
};

/**
 * 验证文章表单数据
 */
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

/**
 * 清理代码块中的多余空格
 */
const cleanCodeContent = (content: string): string => {
  return content.replace(/(\s*)<\/code>/g, "</code>");
};

/**
 * 新增文章
 */
const addArticle = async () => {
  if (!validateArticle()) return;

  try {
    const cleanedContent = cleanCodeContent(editorHtml.value);

    // TODO: 替换为真实 API；失败时请 throw 或设置 resultPhase 为 'fail'
    // const res = await ArticleService.addArticle({ ... })
    // if (res.code !== ApiStatus.success) throw new Error(res.msg)

    console.log("新增文章:", { cleanedContent });

    await new Promise<void>((resolve) => setTimeout(resolve, 400));
    resultPhase.value = "success";
    scrollToTop();
  } catch (error) {
    console.error("发布文章失败:", error);
    resultPhase.value = "fail";
    scrollToTop();
  }
};

/**
 * 编辑文章
 */
const editArticle = async () => {
  if (!validateArticle()) return;

  try {
    const cleanedContent = cleanCodeContent(editorHtml.value);

    // TODO: 替换为真实 API；失败时请 throw 或设置 resultPhase 为 'fail'
    // const res = await ArticleService.editArticle({ ... })
    // if (res.code !== ApiStatus.success) throw new Error(res.msg)

    console.log("编辑文章:", { cleanedContent });

    await new Promise<void>((resolve) => setTimeout(resolve, 400));
    resultPhase.value = "success";
    scrollToTop();
  } catch (error) {
    console.error("保存文章失败:", error);
    resultPhase.value = "fail";
    scrollToTop();
  }
};

/**
 * 提交表单（新增或编辑）
 */
const submit = () => {
  if (pageMode.value === PageModeEnum.Edit) {
    editArticle();
  } else {
    addArticle();
  }
};

/**
 * 图片上传成功回调
 */
const onSuccess = (response: UploadResponse) => {
  cover.value = response.data.url;
  ElMessage.success(`图片上传成功 ${EmojiText[200]}`);
};

/**
 * 图片上传失败回调
 */
const onError = () => {
  ElMessage.error(`图片上传失败 ${EmojiText[500]}`);
};

/**
 * 上传前的文件校验
 */
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

onMounted(() => {
  scrollToTop();
  getArticleTypes();
  initPageMode();
});
</script>
