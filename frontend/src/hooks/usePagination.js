import { usePaginationStore } from '@/stores/pagination'

export default function(getDataCallback, searchRef, sortRef) {
  const route = useRoute()
  const router = useRouter()
  const paginationStore = usePaginationStore()
  const loading = ref(false)
  const currentPage = ref(Number(route.query.page) || 1)
  const currentSize = ref(Number(route.query.size) || 10)
  const totalVisible = ref()

  watch(
    () => route.query,
    async (newQuery, _) => {
      // 只有 page size 有用，搜尋及排序就不修了。
      if (newQuery.page) {
        currentPage.value = parseInt(newQuery.page)
      }
      if (newQuery.size) {
        currentSize.value = parseInt(newQuery.size)
      }
    },
  )

  const getData = async params => {
    let query

    if (paginationStore.reset) {
      query = {}
    } else if (paginationStore.searchBtn) {
      query = params
    } else {
      query = { ...route.query, ...params }
    }

    paginationStore.updateReset(false)
    paginationStore.updateSearchBtn(false)

    await getDataCallback({
      ...query,
      page: currentPage.value,
      size: currentSize.value,
    })
    await router.push({
      query: {
        ...query,
        page: currentPage.value,
        size: currentSize.value,
      },
    })
  }

  const loadData = async ({ page, itemsPerPage, sortBy, search }) => {
    loading.value = true
    currentPage.value = page
    currentSize.value = itemsPerPage

    const params = search ? JSON.parse(search) : {}

    if (sortBy.length) {
      sortBy.forEach((item, i) => {
        const field = item.key.includes('.') ? item.key.split('.')[1] : item.key

        params[`${field}Num`] = i
        params[`${field}Sort`] = item.order === 'desc'
      })
    } else {
      for (const key in route.query) {
        if (key.endsWith('Sort') || key.endsWith('Num')) {
          params[key] = undefined
        }
      }
    }

    await getData(params)

    loading.value = false
  }

  const searchEmit = async params => {
    if (paginationStore.reset) {
      sortRef.value = []
    }
    searchRef.value = JSON.stringify(params)
  }

  onMounted(() => {
    window.onresize = () => {
      totalVisible.value = window.innerWidth >= 600 ? 6 : 3
    }
  })

  return {
    loadData,
    loading,
    currentPage,
    currentSize,
    totalVisible,
    searchEmit,
  }
}
