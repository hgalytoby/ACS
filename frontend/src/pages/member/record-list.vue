<script setup>
import usePagination from '@/hooks/usePagination'
import { useMemberStore } from '@/stores/member'
import { getMemberRecordListFilterFormItems } from '@/utils/filter-form-items'
import { getSortNumQuery } from '@/utils/misc'
import MemberFilterMemberRecordList from '@/views/pages/member/MemberFilterMemberRecordList.vue'

const headers = [
  {
    title: '地點名字', key: 'memberLocationName',
  },
  {
    title: '成員名字', key: 'memberName',
  },
  {
    title: '成員手機', key: 'memberPhone',
  },
  {
    title: '成員公司', key: 'memberCompany',
  },
  {
    title: '成員職稱', key: 'memberJobTitle',
  },
  {
    title: '進出入狀態', key: 'status',
  },
  {
    title: '創建日期', key: 'createdAt',
  },
]

const fieldMappings = {
  status: { num: 'createdAtNum', sort: 'createdAtSort' },
  memberLocationName: { num: 'memberLocationNameNum', sort: 'memberLocationNameSort' },
  memberName: { num: 'memberNameNum', sort: 'memberNameSort' },
  memberPhone: { num: 'memberPhoneNum', sort: 'memberPhoneSort' },
  memberCompany: { num: 'memberCompanyNum', sort: 'memberCompanySort' },
  memberJobTitle: { num: 'memberJobTitleNum', sort: 'memberJobTitleSort' },
  createdAt: { num: 'createdAtNum', sort: 'createdAtSort' },
}

const memberStore = useMemberStore()
const search = ref(JSON.stringify(getMemberRecordListFilterFormItems()))
const sortBy = ref(getSortNumQuery(fieldMappings))

const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
  searchEmit,
} = usePagination(memberStore.memberRecordList, search, sortBy)
</script>

<template>
  <div class="pa-3">
    <MemberFilterMemberRecordList @search-emit="searchEmit" />
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
