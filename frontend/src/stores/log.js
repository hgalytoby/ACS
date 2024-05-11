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
        this.$patch({ users: data })
      })
    },
    async logSystems(params) {
      await reqLogSystems(params).then(({ data }) => {
        this.$patch({ systems: data })
      })
    },
  },
})
