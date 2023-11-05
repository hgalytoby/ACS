<script setup>
import AuthProvider from '@/views/pages/authentication/AuthProvider.vue'
</script>

<template>
  <VCard
    class="auth-card pa-4 pt-7"
    max-width="448"
  >
    <VCardItem class="justify-center">
      <template #prepend>
        <VIcon
          icon="mdi-door-sliding-lock"
          color="primary"
          size="30px"
        />
      </template>

      <VCardTitle class="font-weight-semibold">
        <span class="d-none d-sm-block">Access Control System</span>
        <span class="d-sm-none">ACS</span>
      </VCardTitle>
    </VCardItem>

    <VCardText class="pt-2">
      <slot name="header" />
    </VCardText>

    <VCardText>
      <slot name="content" />
    </VCardText>
    <VRow>
      <VCol
        cols="12"
        class="d-flex align-center my-n5"
      >
        <VDivider />
        <span class="mx-4">or</span>
        <VDivider />
      </VCol>
      <VCol
        cols="12"
        class="my-n3 text-center"
      >
        <AuthProvider />
      </VCol>
    </VRow>
  </VCard>
</template>


