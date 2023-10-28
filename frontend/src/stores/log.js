import { defineStore } from 'pinia'
import {
  reqLogUsers,
  reqLogSystems,
} from '@/api/log'
import defaultAvatar from '@images/avatars/default-avatar.png'

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
    async logSystems() {
      await reqLogSystems().then(({ data }) => {
        this.$patch({ systems: data })
      })
    },
  },
})
