<template>
  <div>
    <ElForm @submit.prevent="addComment" class="w-full mx-auto mb-10">
      <ElFormItem prop="author" class="mt-5">
        <ElInput
          v-model="newComment.author"
          placeholder="你的名称"
          class="block w-full"
          clearable
        />
      </ElFormItem>
      <ElFormItem prop="content">
        <ElInput
          v-model="newComment.content"
          placeholder="简单说两句..."
          type="textarea"
          :rows="5"
          clearable
        />
      </ElFormItem>
      <ElFormItem>
        <div class="flex justify-end w-full">
          <ElButton type="primary" @click="addComment">发布</ElButton>
        </div>
      </ElFormItem>
    </ElForm>

    <ul>
      <div class="pb-5 text-lg font-medium">评论 {{ internalComments.length }}</div>
      <FaCommentItem
        v-for="comment in internalComments.slice().reverse()"
        :key="comment.id"
        :comment="comment"
        :show-reply-form="showReplyForm"
        @toggle-reply="toggleReply"
        @add-reply="addReply"
        class="pb-2.5 mb-5 border-b border-g-400"
      />
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";

interface Comment {
  id: number;
  author: string;
  content: string;
  timestamp: string;
  replies: Comment[];
}

const mockCommentList: Comment[] = [
  {
    id: 1,
    author: "白夜",
    content: "黑神话悟空的打斗场面真的燃爆了！期待上线！",
    timestamp: "2024-09-04 09:00",
    replies: [
      {
        id: 101,
        author: "星河",
        content: "是啊，特别是那些技能特效，简直帅炸！",
        timestamp: "2024-09-04 09:15",
        replies: [],
      },
    ],
  },
];

defineOptions({ name: "FaCommentWidget" });

interface Props {
  /** 评论列表数据，不传则使用 mock 数据 */
  comments?: Comment[];
}

const props = withDefaults(defineProps<Props>(), {
  comments: () => [],
});

interface Emits {
  "add-comment": [comment: Comment];
  "add-reply": [commentId: number, author: string, content: string];
}

const emit = defineEmits<Emits>();

/** 内部评论数据（优先使用 props，否则使用 mock 数据） */
const internalComments = ref<Comment[]>(
  props.comments.length > 0 ? props.comments : mockCommentList
);

const newComment = ref<Partial<Comment>>({
  author: "",
  content: "",
});

const showReplyForm = ref<number | null>(null);

const addComment = () => {
  if (!newComment.value.author?.trim() || !newComment.value.content?.trim()) {
    ElMessage.warning("请填写完整的评论信息");
    return;
  }

  const newCommentData: Comment = {
    id: Date.now(),
    author: newComment.value.author.trim(),
    content: newComment.value.content.trim(),
    timestamp: new Date().toISOString(),
    replies: [],
  };

  internalComments.value.push(newCommentData);

  newComment.value.author = "";
  newComment.value.content = "";
  emit("add-comment", newCommentData);
  ElMessage.success("评论发布成功");
};

const addReply = (commentId: number, replyAuthor: string, replyContent: string) => {
  if (!replyAuthor?.trim() || !replyContent?.trim()) {
    ElMessage.warning("请填写完整的回复信息");
    return;
  }

  const comment = findComment(internalComments.value, commentId);
  if (comment) {
    comment.replies.push({
      id: Date.now(),
      author: replyAuthor.trim(),
      content: replyContent.trim(),
      timestamp: new Date().toISOString(),
      replies: [],
    });
    showReplyForm.value = null;
    emit("add-reply", commentId, replyAuthor, replyContent);
    ElMessage.success("回复发布成功");
  }
};

const toggleReply = (commentId: number) => {
  showReplyForm.value = showReplyForm.value === commentId ? null : commentId;
};

const findComment = (comments: Comment[], commentId: number): Comment | undefined => {
  for (const comment of comments) {
    if (comment.id === commentId) {
      return comment;
    }
    const found = findComment(comment.replies, commentId);
    if (found) {
      return found;
    }
  }
  return undefined;
};
</script>
