import { defineStore } from 'pinia'

export const usePaginationStore = defineStore({
  id: 'usePaginationStore',
  state: () => ({
    reset: false,
  }),
  actions: {
    updateReset(payload){
      this.$patch({
        reset: payload,
      })
    },
  },
})
