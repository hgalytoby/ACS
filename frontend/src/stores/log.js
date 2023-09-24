import { defineStore } from 'pinia'
import {
  reqLogUsers,
  reqLogSystems,
} from '@/api/log'

export const useLogStore = defineStore({
  id: 'useLogStore',
  state: () => ({
    users: {
      items: [],
      pages: 1,
      total: 1,
    },
    systems: {
      items: [],
      pages: 1,
      total: 1,
    },
  }),
  actions: {
    async logUsers(params) {
      await reqLogUsers(params).then(({ data }) => {
        data.items.forEach(item => item.rawData = JSON.stringify(item.rawData))
        this.$patch({ users: data })
      })
    },
    async logSystems() {
      await reqLogSystems().then(({ data }) => {
        this.$patch({ systems: data })
      })
    },
  },
})
