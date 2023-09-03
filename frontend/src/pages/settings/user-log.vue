<script setup>
import usePagination from '@/hooks/usePagination'
import SettingsUserLogFilterLog from '@/views/pages/settings/SettingsUserLogFilterLog.vue'
import { useLogStore } from '@/stores/log'
import SettingsUserLogDialogs from '@/views/pages/settings/SettingsUserLogDialogs.vue'

const headers = [
  {
    title: '查看', key: 'user', class: 'rounded-lg',
  },
  {
    title: '事件', key: 'event', class: 'rounded-lg',
  },
  {
    title: '使用者信箱', key: 'user.email', class: 'rounded-lg',
  },
  {
    title: '使用者名稱', key: 'user.username', class: 'rounded-lg',
  },
  { title: '原始資料', key: 'rawData', sortable: false },
  {
    title: '建立時間', key: 'createdAt', class: 'rounded-lg',
  },
]

const sortBy = ref([{ key: 'calories', order: 'asc' }])
const logStore = useLogStore()
const route = useRoute()
const dialog = ref(null)
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
} = usePagination(logStore.logUsers)

const searchEmit = async params => {
  search.value = JSON.stringify(params)
}

const openDialog = userinfo => {
  dialog.value.openDialog(userinfo)
}
</script>

<template>
  <div class="pa-3">
    <SettingsUserLogFilterLog @search-emit="searchEmit" />
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
        :items="logStore.users.items"
        :items-length="logStore.users.total"
        :loading="loading"
        multi-sort
        @update:options="loadData"
      >
        <template #item.user="{ item }">
          <VBtn
            icon="mdi-account-eye"
            variant="text"
            color="secondary"
            @click="openDialog(item.columns.user)"
          />
        </template>
        <template #bottom>
          <VRow class="text-center px-2 pa-2">
            <VCol
              sm="10"
              cols="12"
            >
              <VPagination
                v-model="currentPage"
                :length="logStore.users.pages"
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
                @update:model-value="currentSize = $event"
              />
            </VCol>
          </VRow>
        </template>
      </VDataTableServer>
    </VCard>
    <SettingsUserLogDialogs ref="dialog" />
  </div>
</template>
