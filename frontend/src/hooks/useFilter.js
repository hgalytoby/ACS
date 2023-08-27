
export default function(emit) {
  const submitBtnLoading = ref(false)

  const submit = payload => {
    submitBtnLoading.value = true
    emit('searchEmit', payload)
    submitBtnLoading.value = false
  }

  
  return {
    emit,
    submit,
  }
}
