
export default function(emit) {
  const submitBtnLoading = ref(false)

  const submit = payload => {
    submitBtnLoading.value = true

    const result = {}

    Object.keys(payload).forEach(key => {
      if (payload[key] !== '') {
        result[key] = payload[key]
      }
    })
    emit('searchEmit', result)
    submitBtnLoading.value = false
  }

  
  return {
    emit,
    submit,
  }
}
