import { usePaginationStore } from '@/stores/pagination'

export default function(emit, formItems, initItems) {
  const paginationStore = usePaginationStore()
  const myForm = ref(null)

  const setFormValue = () => {
    for (const key in formItems) {
      myForm.value.setFieldValue(key, formItems[key])
    }
  }

  const resetForm = () => {
    for (const key in initItems) {
      formItems[key] = initItems[key]
    }
    setFormValue()
    paginationStore.updateReset(true)
    emit('searchEmit')
  }

  const submit = payload => {
    const result = {}

    Object.keys(payload).forEach(key => {
      if (payload[key]?.length !== 0) {
        result[key] = payload[key]
      }
    })
    paginationStore.updateSearchBtn(true)
    emit('searchEmit', result)
  }

  onMounted(async () => {
    setFormValue()
  })
  
  return {
    myForm,
    resetForm,
    submit,
  }
}
