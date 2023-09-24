<script setup>
import { useUserStore } from '@/stores/user'
import AccountSettingsFilterLog from '@/views/pages/account-settings/AccountSettingsFilterLog.vue'
import usePagination from '@/hooks/usePagination'
import { getSortNumQuery } from '@/utils/misc'
import { getAccountSettingsUserListFilterFormItems } from '@/utils/filter-form-items'

const headers = [
  {
    title: '事件', key: 'event', width: '15%', class: 'rounded-lg',
  },
  { title: '原始資料', key: 'rawData', sortable: false },
  {
    title: '建立時間', key: 'createdAt', width: '20%', class: 'rounded-lg',
  },
]

const fieldMappings = {
  createdAt: { num: 'createdAtNum', sort: 'createdAtSort' },
  event: { num: 'eventNum', sort: 'eventSort' },
}

const userStore = useUserStore()
const route = useRoute()
const search = ref(JSON.stringify(getAccountSettingsUserListFilterFormItems()))
const sortBy = ref(getSortNumQuery(fieldMappings))

const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
  searchEmit,
} = usePagination(userStore.userLog, search, sortBy)
</script>

<template>
  <div class="pa-3">
    <AccountSettingsFilterLog @search-emit="searchEmit" />
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
        :items="userStore.log.items"
        :items-length="userStore.log.total"
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
                :length="userStore.log.pages"
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
  </div>
</template>
