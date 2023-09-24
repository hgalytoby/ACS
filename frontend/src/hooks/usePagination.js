import { usePaginationStore } from '@/stores/pagination'

export default function(getDataCallback, searchRef, sortRef) {
  const route = useRoute()
  const router = useRouter()
  const paginationStore = usePaginationStore()
  const loading = ref(false)
  const currentPage = ref(Number(route.query.page) || 1)
  const currentSize = ref(Number(route.query.size) || 25)
  const totalVisible = ref()

  const getData = async params => {
    const query = paginationStore.reset ? {} : { ...route.query, ...params }

    paginationStore.updateReset(false)

    await getDataCallback({
      ...query,
      page: currentPage.value,
      size: currentSize.value,
    })
    query.tab = route.query.tab
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
    console.log(sortBy)

    const params = search ? JSON.parse(search) : {}

    sortBy.forEach((item, i) => {
      const field = item.key.includes('.') ? item.key.split('.')[1] : item.key

      params[`${field}Num`] = i
      params[`${field}Sort`] = item.order === 'asc'
    })
    console.log(params)

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
