export default function(getDataCallback) {
  const route = useRoute()
  const router = useRouter()
  const loading = ref(false)
  const currentPage = ref(Number(route.query.page) || 1)
  const currentSize = ref(Number(route.query.size) || 25)

  const getData = async params => {
    await getDataCallback({
      page: currentPage.value,
      size: currentSize.value,
      ...params,
    })
    await router.push({
      query: {
        ...route.query,
        ...params,
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

    sortBy.forEach((item, i) => {
      params[`${item.key}Num`] = i
      params[`${item.key}Sort`] = item.order === 'asc'
    })

    await getData(params)

    loading.value = false
  }

  return {
    loadData,
    loading,
    currentPage,
    currentSize,
  }
}
