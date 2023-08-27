<script setup>
import { useRoute } from 'vue-router'
import log from '@/pages/account-settings/log.vue'
import security from '@/pages/account-settings/security.vue'
import account from '@/pages/account-settings/account.vue'

const route = useRoute()
const router = useRouter()
const activeTab = ref(route.query.tab || 'account')

router.push({
  // params: { tab: activeTab.value },
  query: { tab: activeTab.value,  ...route.query }, 
})

const tabs = [
  {
    title: 'Account',
    icon: 'mdi-account-outline',
    tab: 'account',
    component: account,
  },
  {
    title: 'Security',
    icon: 'mdi-lock-open-outline',
    tab: 'security',
    component: security,
  },
  {
    title: 'Log',
    icon: 'mdi-book-open-variant',
    tab: 'log',
    component: log,
  },
]

const tabEvent = tab => {
  console.log(tab, { tab: tab,  ...route.query })
  router.push({ query: { ...route.query, tab } })
}

watch(route, (nV, _) => {
  console.log(nV.query.tab)
  activeTab.value = nV.query.tab || 'account'
})
</script>

<template>
  <div>
    <VTabs
      v-model="activeTab"
      show-arrows
      @update:model-value="tabEvent"
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
