<script setup>
import { useRoute } from 'vue-router'
import loginFail from '@/pages/settings/email-message/login-fail.vue'
import forgotPassword from '@/pages/settings/email-message/forgot-password.vue'
import destroy from '@/pages/settings/email-message/destory.vue'
import resetPassword from '@/pages/settings/email-message/reset-password.vue'
import verify from '@/pages/settings/email-message/verify.vue'
import register from '@/pages/settings/email-message/register.vue'
import { useEmailStore } from '@/stores/email'

const route = useRoute()
const router = useRouter()
const activeTab = ref(route.query.tab || 'register')
const emailStore = useEmailStore()

emailStore.settingList()
router.push({
  // params: { tab: activeTab.value },
  query: { tab: activeTab.value,  ...route.query },
})

const tabs = [
  {
    title: '使用者註冊設定',
    tab: 'register',
    component: register,
    icon: 'mdi-account-plus-outline',
  },
  {
    title: '使用者忘記密碼設定',
    tab: 'forgotPassword',
    component: forgotPassword,
    icon: 'mdi-lock-question',
  },
  {
    title: '使用者重置密碼設定',
    tab: 'resetPassword',
    component: resetPassword,
    icon: 'mdi-lock-reset',
  },
  {
    title: '驗證使用者設定',
    tab: 'verify',
    component: verify,
    icon: 'mdi-account-sync-outline',
  },
  {
    title: '使用者刪除設定',
    tab: 'destroy',
    component: destroy,
    icon: 'mdi-account-remove-outline',
  },
  {
    title: '使用者登入失敗設定',
    tab: 'loginFail',
    component: loginFail,
    icon: 'mdi-account-question-outline',
  },
]

const tabEvent = tab => {
  router.push({ query: { ...route.query, tab } })
}

watch(route, (nV, _) => {
  activeTab.value = nV.query.tab || 'register'
})
</script>

<template>
  <div>
    <VTabs
      v-model="activeTab"
      next-icon="mdi-chevron-right"
      prev-icon="mdi-chevron-left"
      align-tabs="center"
      show-arrows
      center-active
      grow
      stacked
      @update:model-value="tabEvent"
    >
      <VTab
        v-for="item in tabs"
        :key="item.icon"
        :value="item.tab"
      >
        <v-icon :icon="item.icon" />
        <span class="d-none d-md-block">{{ item.title }}</span>
      </VTab>
    </VTabs>
    <VDivider />
    <VWindow
      v-model="activeTab"
      class="mt-5"
    >
      <VWindowItem
        v-for="tab in tabs"
        :key="tab.tab"
        :value="tab.tab"
      >
        <Component :is="tab.component" />
      </vwindowitem> 
    </VWindow> 
  </div>
</template>
