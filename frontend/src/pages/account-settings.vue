<script setup>
import { useRoute } from 'vue-router'
import AccountSettingsAccount from '@/views/pages/account-settings/AccountSettingsAccount.vue'
import AccountSettingsSecurity from '@/views/pages/account-settings/AccountSettingsSecurity.vue'
import AccountSettingsLog from '@/views/pages/account-settings/AccountSettingsLog.vue'

const route = useRoute()
const activeTab = ref(route.params.tab)

// tabs
const tabs = [
  {
    title: 'Account',
    icon: 'mdi-account-outline',
    tab: 'account',
    component: AccountSettingsAccount,
  },
  {
    title: 'Security',
    icon: 'mdi-lock-open-outline',
    tab: 'security',
    component: AccountSettingsSecurity,

  },
  {
    title: 'Log',
    icon: 'mdi-book-open-variant',
    tab: 'log',
    component: AccountSettingsLog,

  },
]
</script>

<template>
  <div>
    <VTabs
      v-model="activeTab"
      show-arrows
    >
      <VTab
        v-for="item in tabs"
        :key="item.icon"
        :value="item.tab"
      >
        <VIcon
          size="20"
          start
          :icon="item.icon"
        />
        {{ item.title }}
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
