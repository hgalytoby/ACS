<script setup>
import { useUserStore } from '@/stores/user'
import MyVImg from '@/components/MyVImg.vue'

const dialog = ref(false)
const userStore = useUserStore()

const openDialog = async payload => {
  dialog.value = true
  await userStore.userInfo(payload.id)
}

const updateDialogEvent = () => {
  userStore.resetUserInfo()
}

defineExpose({
  openDialog,
})
</script>

<template>
  <div class="text-center">
    <VDialog
      v-model="dialog"
      width="auto"
      @update:model-value="updateDialogEvent"
    >
      <VCard class="py-3">
        <div class="ma-auto">
          <MyVImg
            :img-obj="{
              class: 'rounded',
              width: '200', 
              src: userStore.user.avatar,
            }"
          />
        </div>
        <VCardItem>
          <VCardTitle>使用者資料</VCardTitle>
        </VCardItem>
        <VCardText>
          <VIcon icon="mdi-account" />
          username: {{ userStore.user.username }}
        </VCardText>
        <VCardText>
          <VIcon icon="mdi-email" />
          email: {{ userStore.user.email }}
        </VCardText>
        <VCardText>
          <VIcon icon="mdi-calendar" />
          createdAt: {{ userStore.user.createdAt }}
        </VCardText>
        <VCardText>
          <VIcon icon="mdi-shield-account" />
          Roles:
          <v-chip
            v-for="role in userStore.meInfo.roleList"
            :key="role.id"
            class="ms-2"
            color="primary"
          >
            {{ role.name }}
          </v-chip>
        </VCardText>
        <VCardText>
          <VIcon icon="mdi-link" />
          Link:

          <VIcon
            v-for="oauth in userStore.meInfo.oauthAccounts"
            :key="oauth.id"
            class="mx-1"
            :icon="`mdi-${oauth.oauthName}`"
          />
        </VCardText>
      </VCard>
    </VDialog>
  </div>
</template>

