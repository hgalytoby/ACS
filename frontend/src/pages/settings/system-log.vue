<script setup>
import { useLogStore } from '@/stores/log'
import { getSystemLogFilterFormItems } from '@/utils/filter-form-items'
import { getSortNumQuery } from '@/utils/misc'
import usePagination from '@/hooks/usePagination'
import SettingsSystemFilterLog from '@/views/pages/settings/SettingsSystemFilterLog.vue'

const logStore = useLogStore()

const headers = [
  {
    title: '事件', key: 'event',
  },
  {
    title: '創建日期', key: 'createdAt',
  },
]

const fieldMappings = {
  createdAt: { num: 'createdAtNum', sort: 'createdAtSort' },
  event: { num: 'eventNum', sort: 'eventSort' },
}

const search = ref(JSON.stringify(getSystemLogFilterFormItems()))
const sortBy = ref(getSortNumQuery(fieldMappings))

const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
  searchEmit,
} = usePagination(logStore.logSystems, search, sortBy)
</script>

<template>
  <div class="pa-3">
    <SettingsSystemFilterLog @search-emit="searchEmit" />
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
        :items="logStore.systems.items"
        :items-length="logStore.systems.total"
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
                :length="logStore.systems.pages"
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
