<script setup>
import Base from '@/views/pages/settings/email-settings/Base.vue'
import { useHealthStore } from '@/stores/health'
import * as yup from 'yup'

const url = `${window.location.protocol}//${window.location.host}/auth/verify?token=abc123`
const healthStore = useHealthStore()

const show = value => {
  if (value && value.includes('{url}')){
    return value.replace('{url}', url)
  } else {
    return `需要有 {url} 值! \n\n範例: ${healthStore.project} 使用者註冊信 網址: ${url}`
  }
}

const bodyRule = {
  show,
  schema: yup.string().required().test({
    name: 'include {url}',
    message: '格式錯誤!',
    test: value => value.includes('{url}'),
  }),
}
</script>

<template>
  <Base
    event="UserRegister"
    :body-rule
  />
</template>
