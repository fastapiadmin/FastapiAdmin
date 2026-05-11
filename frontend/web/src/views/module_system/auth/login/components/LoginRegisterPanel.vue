<!-- 注册表单 -->
<template>
  <div>
    <ElForm
      ref="formRef"
      :model="registerForm"
      :rules="registerRules"
      :key="formKey"
      class="login-page-form"
      @keyup.enter="$emit('submit')"
    >
      <ElFormItem prop="username">
        <ElInput
          class="custom-height"
          v-model.trim="registerForm.username"
          clearable
          :placeholder="$t('login.placeholder.username')"
        >
          <template #prefix>
            <ElIcon><User /></ElIcon>
          </template>
        </ElInput>
      </ElFormItem>
      <ElTooltip :visible="isCapsLock" :content="$t('login.capsLock')" placement="right">
        <ElFormItem prop="password">
          <ElInput
            class="custom-height"
            v-model.trim="registerForm.password"
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
            class="custom-height"
            v-model.trim="registerForm.confirmPassword"
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
      <ElFormItem>
        <div class="flex flex-wrap items-center gap-2">
          <ElCheckbox v-model="registerAgreementReadModel">
            {{ $t("login.agree") }}
          </ElCheckbox>
          <ElLink
            type="primary"
            :underline="false"
            class="text-sm font-medium"
            :href="userAgreementHref"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ $t("login.userAgreement") }}
          </ElLink>
        </div>
      </ElFormItem>
      <div class="mt-6">
        <ElButton
          class="h-11 w-full !rounded-lg text-base font-medium"
          type="primary"
          :loading="registerLoading"
          v-ripple
          @click="$emit('submit')"
        >
          {{ $t("login.register") }}
        </ElButton>
      </div>
    </ElForm>

    <LoginAuthLinkRow
      :hint="$t('login.haveAccount')"
      :link-text="$t('login.backLoginBtnText')"
      @link="$emit('toLogin')"
    />
  </div>
</template>

<script setup lang="ts">
import { Lock, User } from "@element-plus/icons-vue";
import type { RegisterForm } from "@/api/module_system/user";
import type { FormRules } from "element-plus";
import LoginAuthLinkRow from "./LoginAuthLinkRow.vue";

defineProps<{
  registerForm: RegisterForm;
  registerRules: FormRules<RegisterForm>;
  formKey: number | string;
  registerLoading: boolean;
  userAgreementHref: string;
}>();

const registerAgreementReadModel = defineModel<boolean>("registerAgreementRead", {
  required: true,
});

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
  validateField: (prop: string | string[]) => formRef.value?.validateField?.(prop),
});
</script>

<style scoped>
@import "../style.css";
</style>
