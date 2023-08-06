<script setup>
import { useUserStore } from '@/stores/user'
import AccountSettingsFilterLog from '@/views/pages/account-settings/AccountSettingsFilterLog.vue'

const userStore = useUserStore()

const options = reactive({})
const loading = ref(false)
const totalVisible = ref()
const search = ref()

const headers = [
  {
    title: '事件', key: 'event', width: '15%', class: 'rounded-lg',
  },
  { title: '原始資料', key: 'rawData', sortable: false },
  {
    title: '建立時間', key: 'createdAt', width: '20%', class: 'rounded-lg',
  },
]

const searchEmit = async params => {
  console.log('emitSearch', params)
  search.value = JSON.stringify(params)
}

const getData = async (page = 1, size = 10, params) => {
  await userStore.userLog({ page, size, ...params })
}

const loadData = async ({ page, itemsPerPage, sortBy, search }) => {
  const params = search ? JSON.parse(search) : {}
  console.log('loadData', params)
  sortBy.forEach((item, i) => {
    params[`${item.key}Num`] = i
    params[`${item.key}Sort`] = item.order === 'asc'
  })
  loading.value = true
  await getData(page, itemsPerPage, params)
  loading.value = false
}

const test = async () => {
  search.value = '213'
}

onMounted(() => {
  window.onresize = () => {
    totalVisible.value = window.innerWidth >= 600 ? 6 : 3
  }
})
</script>

<template>
  <div class="pa-3">
    <button @click="test">
      test
    </button>
    <AccountSettingsFilterLog @search-emit="searchEmit" />
    <VCard
      class="mt-5"
      elevation="3"
      rounded="lg"
    >
      <VDataTableServer
        v-model:items-per-page="userStore.log.size"
        v-model:page="userStore.log.page"
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
                v-model="userStore.log.page"
                :length="userStore.log.pages"
                :total-visible="totalVisible"
              />
            </VCol>
            <VCol
              sm="2"
              cols="12"
            >
              <VSelect
                :model-value="userStore.log.size"
                label="顯示比數"
                :items="[10, 25, 50]"
                density="compact"
                hide-details
                @update:model-value="userStore.log.size = $event"
              />
            </VCol>
          </VRow>
        </template>
      </VDataTableServer>
    </VCard>
  </div>
</template>
