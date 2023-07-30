import { defineStore } from 'pinia'
import { reqHealth } from '@/api/health'

export const useHealthStore = defineStore({
  id: 'useHealthStore',
  state: () => ({
    project: '',
  }),
  actions: {
    async health() {
      await reqHealth().then(({ data }) => {
        this.$patch({ project: data.project })
      })
    },
  },
},
)
