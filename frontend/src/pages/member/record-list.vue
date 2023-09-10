<script setup>
import usePagination from '@/hooks/usePagination'
import { useMemberStore } from '@/stores/member'
import SettingsUserListFilterLog from '@/views/pages/settings/SettingsUserListFilterLog.vue'

const headers = [
]

const memberStore = useMemberStore()
const route = useRoute()
const router = useRouter()

const search = ref(JSON.stringify({
  createdAt: route.query.createdAt,
}))

const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
} = usePagination(memberStore.memberRecordList)

const searchEmit = params => {
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
        :items="memberStore.list.items"
        :items-length="memberStore.list.total"
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
                :length="memberStore.list.pages"
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

<style scoped lang='scss'>

</style>
