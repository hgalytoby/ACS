<script setup>
import usePagination from '@/hooks/usePagination'
import SettingsUserLogFilterLog from '@/views/pages/settings/SettingsUserLogFilterLog.vue'
import { useLogStore } from '@/stores/log'
import SettingsUserLogDialogs from '@/views/pages/settings/SettingsUserLogDialogs.vue'
import { getSortNumQuery } from '@/utils/misc'

const headers = [
  {
    title: '查看', key: 'user', sortable: false,
  },
  {
    title: '事件', key: 'event',
  },
  {
    title: '使用者信箱', key: 'user.email',
  },
  {
    title: '使用者名稱', key: 'user.username',
  },
  { 
    title: '原始資料', key: 'rawData', sortable: false,
  },
  {
    title: '建立時間', key: 'createdAt',
  },
]

const fieldMappings = {
  createdAt: { num: 'createdAtNum', sort: 'createdAtSort' },
  'user.username': { num: 'usernameNum', sort: 'usernameSort' },
  'user.email': { num: 'emailNum', sort: 'emailSort' },
  event: { num: 'eventNum', sort: 'eventSort' },
}

const logStore = useLogStore()
const search = ref()
const sortBy = ref(getSortNumQuery(fieldMappings))
const dialog = ref(null)


const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
  searchEmit,
} = usePagination(logStore.logUsers, search, sortBy)

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
        v-model:sort-by="sortBy"
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
