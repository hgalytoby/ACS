import { defineStore } from 'pinia'

export const usePaginationStore = defineStore({
  id: 'usePaginationStore',
  state: () => ({
    reset: false,
    searchBtn: false,
  }),
  actions: {
    updateReset(payload){
      this.$patch({
        reset: payload,
      })
    },
    updateSearchBtn(payload){
      this.$patch({
        searchBtn: payload,
      })
    },
  },
})
