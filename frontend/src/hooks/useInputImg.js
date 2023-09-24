export default function(resetCallback) {
  const refInputEl = ref()
  const imgModel = ref()

  const changeImg = file => {
    const fileReader = new FileReader()
    const { files } = file.target

    if (files && files.length) {
      fileReader.readAsDataURL(files[0])
      fileReader.onload = () => {
        if (typeof fileReader.result === 'string')
          imgModel.value = fileReader.result
      }
    }
  }

  const resetImgModel = () => {
    refInputEl.value.value = null
    imgModel.value = undefined
    if (resetCallback) {
      resetCallback()
    }
  }

  return {
    refInputEl,
    imgModel,
    changeImg,
    resetImgModel,
  }
}

