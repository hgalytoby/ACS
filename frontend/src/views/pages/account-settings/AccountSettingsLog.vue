<script setup>
import { useUserStore } from '@/stores/user'
import AccountSettingsFilterLog from '@/views/pages/account-settings/AccountSettingsFilterLog.vue'

const userStore = useUserStore()

const getData = async () => userStore.userLog()

onMounted(async () => {
  await getData()
})
</script>

<template>
  <div class="pa-3">
    <AccountSettingsFilterLog />
    <VCard
      class="mt-5"
      elevation="3"
      rounded="lg"
    >
      {{ userStore.log }}
    </VCard>
  </div>
</template>
