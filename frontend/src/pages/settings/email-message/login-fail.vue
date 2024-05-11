<script setup>
import Base from '@/views/pages/settings/email-settings/Base.vue'
import * as yup from 'yup'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()

const show = value => {
  if (value && value.includes('{ip}')){
    return value.replace('{ip}', healthStore.clientIp)
  } else {
    return `需要有 {ip} 值! \n\n範例: 您的帳號從 IP: {ip} 多次登入失敗!`
  }
}

const bodyRule = {
  show,
  schema: yup.string().required().test({
    name: 'include {ip}',
    message: '格式錯誤!',
    test: value => value.includes('{ip}'),
  }),
}
</script>

<template>
  <Base
    event="UserLoginFail"
    :body-rule
  />
</template>
