<script setup>
import defaultAvatar from '@images/avatars/default-avatar.png'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import ImageLazyProgress from '@/components/ImageLazyProgress.vue'

const authStore = useAuthStore()
const userStore = useUserStore()

async function logout() {
  await authStore.logout()
}

const avatar = computed(() => userStore.me.avatar || defaultAvatar)
</script>

<template>
  <VBadge
    dot
    location="bottom right"
    offset-x="3"
    offset-y="3"
    color="success"
    bordered
  >
    <VAvatar
      class="cursor-pointer"
      color="primary"
      variant="tonal"
    >
      <VImg
        :src="avatar"
        :lazy-src="avatar"
      >
        <template #placeholder>
          <ImageLazyProgress />
        </template>
      </VImg>

      <VMenu
        activator="parent"
        width="230"
        location="bottom end"
        offset="14px"
      >
        <VList>
          <VListItem>
            <template #prepend>
              <VListItemAction start>
                <VBadge
                  dot
                  location="bottom right"
                  offset-x="3"
                  offset-y="3"
                  color="success"
                >
                  <VAvatar
                    color="primary"
                    variant="tonal"
                  >
                    <VImg
                      :src="avatar"
                      :lazy-src="avatar"
                    >
                      <template #placeholder>
                        <ImageLazyProgress />
                      </template>
                    </VImg>
                  </VAvatar>
                </VBadge>
              </VListItemAction>
            </template>

            <VListItemTitle class="font-weight-semibold">
              {{ userStore.me.username }}
            </VListItemTitle>
            <VListItemSubtitle>Admin</VListItemSubtitle>
          </VListItem>
          <VDivider class="my-2" />

          <VListItem :to="{name: 'AccountSettings'}">
            <template #prepend>
              <VIcon
                class="me-2"
                icon="mdi-account-outline"
                size="22"
              />
            </template>

            <VListItemTitle>Profile</VListItemTitle>
          </VListItem>

          <VDivider class="my-2" />

          <VListItem @click="logout">
            <template #prepend>
              <VIcon
                class="me-2"
                icon="mdi-logout"
                size="22"
              />
            </template>

            <VListItemTitle>Logout</VListItemTitle>
          </VListItem>
        </VList>
      </VMenu>
    </VAvatar>
  </VBadge>
</template>
