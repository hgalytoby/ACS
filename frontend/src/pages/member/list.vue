<script setup>
import usePagination from '@/hooks/usePagination'
import { useMemberStore } from '@/stores/member'
import MemberFilterMemberList from '@/views/pages/member/MemberFilterMemberList.vue'
import { getSortNumQuery } from '@/utils/misc'
import { getMemberListFilterFormItems } from '@/utils/filter-form-items'
import MyVImg from '@/components/MyVImg.vue'

const headers = [
  {
    title: 'Qrcode', key: 'qrcode', sortable: false,
  },
  {
    title: '圖片', key: 'image', sortable: false,
  },
  {
    title: '名字', key: 'name',
  },
  {
    title: '血型', key: 'bloodType',
  },
  {
    title: '生日', key: 'birthday',
  },
  {
    title: '手機', key: 'phone',
  },
  {
    title: '公司', key: 'company',
  },
  {
    title: '職稱', key: 'jobTitle',
  },
  {
    title: '創建日期', key: 'createdAt',
  },
]

const fieldMappings = {
  createdAt: { num: 'createdAtNum', sort: 'createdAtSort' },
  username: { num: 'usernameNum', sort: 'usernameSort' },
  bloodType: { num: 'bloodTypeNum', sort: 'bloodTypeSort' },
  birthday: { num: 'birthdayNum', sort: 'birthdaySort' },
  phone: { num: 'phoneNum', sort: 'phoneSort' },
  company: { num: 'companyNum', sort: 'companySort' },
  jobTitle: { num: 'jobTitleNum', sort: 'jobTitleSort' },
  event: { num: 'eventNum', sort: 'eventSort' },
}

const memberStore = useMemberStore()
const search = ref(JSON.stringify(getMemberListFilterFormItems()))
const sortBy = ref(getSortNumQuery(fieldMappings))

const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
  searchEmit,
} = usePagination(memberStore.memberList, search, sortBy)
</script>

<template>
  <div class="pa-3">
    <MemberFilterMemberList @search-emit="searchEmit" />
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
        :items="memberStore.list.items"
        :items-length="memberStore.list.total"
        :loading="loading"
        multi-sort
        @update:options="loadData"
      >
        <template #item.qrcode="{ item }">
          <MyVImg
            :img-obj="{
              width: '100px',
              src: item.qrcode,
              lazySrc: item.qrcode,
            }"
          />
        </template>
        <template #item.image="{ item }">
          <MyVImg
            :img-obj="{
              width: '100px',
              src: item.image,
              lazySrc: item.image,
            }"
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

