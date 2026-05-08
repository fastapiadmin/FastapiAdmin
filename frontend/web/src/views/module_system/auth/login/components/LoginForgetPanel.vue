<!-- 重置密码 / 忘记密码 -->
<template>
  <div>
    <ElForm
      ref="formRef"
      :model="forgetForm"
      :rules="forgetRules"
      :key="formKey"
      class="login-page-form mt-4"
      @keyup.enter="$emit('submit')"
    >
      <ElFormItem prop="username">
        <ElInput
          v-model.trim="forgetForm.username"
          class="custom-height"
          clearable
          :placeholder="$t('login.placeholder.username')"
          @keyup.enter="$emit('submit')"
        >
          <template #prefix>
            <ElIcon><User /></ElIcon>
          </template>
        </ElInput>
      </ElFormItem>
      <ElTooltip :visible="isCapsLock" :content="$t('login.capsLock')" placement="right">
        <ElFormItem prop="new_password">
          <ElInput
            v-model.trim="forgetForm.new_password"
            class="custom-height"
            type="password"
            autocomplete="off"
            show-password
            clearable
            :placeholder="$t('login.placeholder.password')"
            @keyup="checkCapsLock"
            @keyup.enter="$emit('submit')"
          >
            <template #prefix>
              <ElIcon><Lock /></ElIcon>
            </template>
          </ElInput>
        </ElFormItem>
      </ElTooltip>
      <ElTooltip :visible="isCapsLock" :content="$t('login.capsLock')" placement="right">
        <ElFormItem prop="confirmPassword">
          <ElInput
            v-model.trim="forgetForm.confirmPassword"
            class="custom-height"
            type="password"
            autocomplete="off"
            show-password
            clearable
            :placeholder="$t('login.message.password.confirm')"
            @keyup="checkCapsLock"
            @keyup.enter="$emit('submit')"
          >
            <template #prefix>
              <ElIcon><Lock /></ElIcon>
            </template>
          </ElInput>
        </ElFormItem>
      </ElTooltip>
      <div class="mt-6">
        <ElButton
          class="h-11 w-full min-w-0 !rounded-lg text-base font-medium"
          type="primary"
          :loading="forgetLoading"
          v-ripple
          @click="$emit('submit')"
        >
          {{ $t("common.confirm") }}
        </ElButton>
      </div>
    </ElForm>

    <LoginAuthLinkRow
      :hint="$t('login.thinkOfPasswd')"
      :link-text="$t('login.backLoginBtnText')"
      @link="$emit('toLogin')"
    />
  </div>
</template>

<script setup lang="ts">
import { Lock, User } from "@element-plus/icons-vue";
import type { ForgetPasswordForm } from "@/api/module_system/user";
import type { FormRules } from "element-plus";
import LoginAuthLinkRow from "./LoginAuthLinkRow.vue";

defineProps<{
  forgetForm: ForgetPasswordForm;
  forgetRules: FormRules<ForgetPasswordForm>;
  formKey: number | string;
  forgetLoading: boolean;
}>();

defineEmits<{ submit: []; toLogin: [] }>();

const formRef = ref();
const isCapsLock = ref(false);

function checkCapsLock(event: KeyboardEvent) {
  if (event instanceof KeyboardEvent) {
    isCapsLock.value = event.getModifierState("CapsLock");
  }
}

defineExpose({
  validate: () => formRef.value?.validate?.(),
  clearValidate: () => formRef.value?.clearValidate?.(),
});
</script>

<style scoped>
@import "../style.css";
</style>
