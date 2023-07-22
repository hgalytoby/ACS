<script setup>
import logo from '@images/logo.svg?raw'
import AuthProvider from '@/views/pages/authentication/AuthProvider.vue'
</script>

<template>
  <VCard
    class="auth-card pa-4 pt-7"
    max-width="448"
  >
    <VCardItem class="justify-center">
      <template #prepend>
        <div class="d-flex">
          <div v-html="logo" />
        </div>
      </template>

      <VCardTitle class="font-weight-semibold text-2xl text-uppercase">
        Materio
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
        class="d-flex align-center"
      >
        <VDivider />
        <span class="mx-4">or</span>
        <VDivider />
      </VCol>
      <VCol
        cols="12"
        class="text-center"
      >
        <AuthProvider />
      </VCol>
    </VRow>
  </VCard>
</template>


