<template>
  <EnhancedDialog
    v-model="dialogVisible"
    width="500px"
    max-height="170px"
    :title="dialogTitle"
    class="v-lock-dialog"
  >
    <div class="lock-dialog-content">
      <!-- 头像 -->
      <img :src="userStore.basicInfo.avatar" alt="" class="lock-dialog-avatar" />
      <!-- 用户名 -->
      <!-- <span class="lock-dialog-name">{{ t('navbar.lock') }}</span> -->
      <span class="lock-dialog-name">{{ userStore.basicInfo.name }}</span>
    </div>
    <el-form ref="lockFormRef" :model="form" :rules="rules">
      <el-form-item :label="t('lock.lockPassword')" prop="password">
        <el-input
          v-model="form.password"
          type="password"
          show-password
          clearable
          @keydown.enter="handleLock"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="handleLock">{{ t("navbar.lock") }}</el-button>
    </template>
  </EnhancedDialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { useLockStore } from "@/store";
import { useI18n } from "vue-i18n";
import type { FormInstance, FormRules } from "element-plus";

import { useUserStore } from "@/store/modules/user.store";
const userStore = useUserStore();

const { t } = useI18n();
const lockStore = useLockStore();

const props = defineProps({
  modelValue: {
    type: Boolean,
  },
});

const emit = defineEmits(["update:modelValue"]);

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => {
    emit("update:modelValue", val);
  },
});

const dialogTitle = ref(t("lock.lockScreen"));
const lockFormRef = ref<FormInstance>();
const form = reactive({
  password: "",
});

const rules: FormRules = {
  password: [{ required: true, message: t("lock.required"), trigger: "blur" }],
};

// 优化后的锁定逻辑
const handleLock = async () => {
  try {
    await lockFormRef.value?.validate();
    dialogVisible.value = false;
    lockStore.setLockInfo({
      isLock: true,
      password: form.password,
    });
  } catch {
    // 验证失败时不执行任何操作
  }
};
</script>

<style lang="scss" scoped>
.v-lock-dialog {
  @media (width <=767px) {
    max-width: calc(100vw - 16px);
  }

  .lock-dialog {
    &-content {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    &-avatar {
      width: 70px;
      height: 70px;
      border-radius: 50%;
    }

    &-name {
      margin: 10px 0;
      font-size: 14px;
      color: var(--top-header-text-color);
    }
  }
}
</style>
