import { defineStore } from 'pinia'
import {
  reqLogUsers,
  reqLogSystems,
  reqLogSystem,
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
    async logUsers() {
      await reqLogUsers().then(({ data }) => {
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
