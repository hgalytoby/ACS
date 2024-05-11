import { defineStore } from 'pinia'
import { reqHealth } from '@/api/health'

export const useHealthStore = defineStore({
  id: 'useHealthStore',
  state: () => ({
    project: '',
    clientIp: '',
  }),
  actions: {
    async health() {
      await reqHealth().then(({ data }) => {
        this.$patch(data)
      })
    },
  },
})
