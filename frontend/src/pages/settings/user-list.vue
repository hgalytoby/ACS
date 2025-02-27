<script setup>
import { useUserStore } from '@/stores/user'
import usePagination from '@/hooks/usePagination'
import SettingsUserListFilterLog from '@/views/pages/settings/SettingsUserListFilterLog.vue'
import { getSortNumQuery } from '@/utils/misc'
import { getSettingsUserListFilterFormItems } from '@/utils/filter-form-items'
import MyVImg from '@/components/MyVImg.vue'

const headers = [
  {
    title: '頭像', key: 'avatar', sortable: false,
  },
  {
    title: '信箱', key: 'email',
  },
  {
    title: '名稱', key: 'username',
  },
  {
    title: '創建日期', key: 'createdAt',
  },
]

const fieldMappings = {
  createdAt: { num: 'createdAtNum', sort: 'createdAtSort' },
  email: { num: 'emailNum', sort: 'emailSort' },
  username: { num: 'usernameNum', sort: 'usernameSort' },
}

const userStore = useUserStore()
const search = ref(JSON.stringify(getSettingsUserListFilterFormItems()))
const sortBy = ref(getSortNumQuery(fieldMappings))

const {
  loadData,
  loading,
  currentPage,
  currentSize,
  totalVisible,
  searchEmit,
} = usePagination(userStore.userList, search, sortBy)
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
        v-model:sort-by="sortBy"
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
        <template #item.avatar="{ item }">
          <VAvatar
            color="primary"
            variant="tonal"
          >
            <MyVImg
              :img-obj="{
                src: item.avatar,
                lazySrc: item.avatar,
              }"
            />
          </VAvatar>
        </template>
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
                @update:model-value="currentSize = $event"
              />
            </VCol>
          </VRow>
        </template>
      </VDataTableServer>
    </VCard>
  </div>
</template>
