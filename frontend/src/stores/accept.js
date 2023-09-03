import { defineStore } from 'pinia'
import {
  reqAcceptLocation,
  reqAcceptApi,
} from '@/api/accept'

export const useAcceptStore = defineStore({
  id: 'useAcceptStore',
  state: () => ({
    acceptLocationList: [],
    member: {},
    acceptApi: null,
  }),
  actions: {
    async acceptLocation() {
      await reqAcceptLocation()
        .then(({ data }) => {
          this.$patch({ acceptLocationList: data })
        }).catch(err => {console.log(err)})
    },
    async acceptApi(memberCome) {
      await reqAcceptApi(memberCome)
        .then(({ data }) => {
          this.$patch({ acceptApi: data.api })
        })
        .catch(err => {})
    },
  },
  getters: {
    acceptLocationMap: state => state.acceptLocationList.reduce((result, item) => {
      result[item.id] = item.name

      return result
    }, {}),
  },
})
