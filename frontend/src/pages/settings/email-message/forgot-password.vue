<script setup>
import Base from '@/views/pages/settings/email-settings/Base.vue'
import * as yup from 'yup'
import { useHealthStore } from '@/stores/health'

const url = `${window.location.protocol}//${window.location.host}/auth/reset-password?token=abc123`
const healthStore = useHealthStore()

const show = value => {
  if (value && value.includes('{url}')){
    return value.replace('{url}', url)
  } else {
    return `需要有 {url} 值! \n\n範例: ${healthStore.project} 忘記密碼信 網址: ${url}`
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
    event="UserForgotPassword"
    :body-rule
  />
</template>
