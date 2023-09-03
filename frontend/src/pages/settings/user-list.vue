<script setup>
import { useUserStore } from '@/stores/user'
import usePagination from '@/hooks/usePagination'
import SettingsUserListFilterLog from '@/views/pages/settings/SettingsUserListFilterLog.vue'

const headers = [
  {
    title: '事件', key: 'event', width: '15%', class: 'rounded-lg',
  },
  { title: '原始資料', key: 'rawData', sortable: false },
  {
    title: '建立時間', key: 'createdAt', width: '20%', class: 'rounded-lg',
  },
]

const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const search = ref(JSON.stringify({
  event: route.query.event,
  createdAt: route.query.createdAt,
}))

const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
} = usePagination(userStore.userList)

const searchEmit = async params => {
  await router.push({
    query: {
      // ...route.query,
      // ...params,
      page: currentPage.value,
      size: currentSize.value,
    },
  })
  search.value = JSON.stringify(params)
}
</script>

<template>
  <div class="pa-3">
    <SettingsUserListFilterLog @search-emit="searchEmit" />
    <VCard
      class="mt-5"
      elevation="3"
      rounded="lg"
    >
      <VDataTableServer
        v-model:items-per-page="currentSize"
        v-model:page="currentPage"
        :search="search"
        :headers="headers"
        :items="userStore.list.items"
        :items-length="userStore.list.total"
        :loading="loading"
        multi-sort
        @update:options="loadData"
      >
        <template #bottom>
          <VRow class="text-center px-2 pa-2">
            <VCol
              sm="10"
              cols="12"
            >
              <VPagination
                v-model="currentPage"
                :length="userStore.list.pages"
                :total-visible="totalVisible"
              />
            </VCol>
            <VCol
              sm="2"
              cols="12"
            >
              <VSelect
                :model-value="currentSize"
                label="顯示比數"
                :items="[10, 25, 50]"
                density="compact"
                hide-details
                @update:model-value="currentSize.value = $event"
              />
            </VCol>
          </VRow>
        </template>
      </VDataTableServer>
    </VCard>
  </div>
</template>
