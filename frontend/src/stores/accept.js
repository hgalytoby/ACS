import { defineStore } from 'pinia'
import {
  reqAcceptLocation,
  reqAcceptApi,
  reqAcceptMemberStatus,
} from '@/api/accept'

export const useAcceptStore = defineStore({
  id: 'useAcceptStore',
  state: () => ({
    acceptLocationList: [],
    member: {
      created: null,
      status: null,
      member: {
        id: null,
        name: null,
        bloodType: null,
        birthday: null,
        phone: null,
        company: null,
        jobTitle: null,
        updatedAt: null,
        createdAt: null,
        image: null,
        qrcode: null,
      },
      memberLocation: {
        id: null,
        name: null,
        updatedAt: null,
        createdAt: null,
        image: null,
      },
    },
    acceptApi: null,
  }),
  actions: {
    async acceptLocation() {
      await reqAcceptLocation()
        .then(({ data }) => {
          this.$patch({ acceptLocationList: data })
        }).catch(err => {console.log(err)})
    },
    async acceptApi() {
      await reqAcceptApi()
        .then(({ data }) => {
          this.$patch({ acceptApi: data.api })
        })
        .catch(err => {})
    },
    async acceptMemberStatus(payload) {
      try {
        await reqAcceptMemberStatus(payload)
          .then(({ data }) => {
            this.$patch({ member: data })
          })
      } catch (err) {
        console.error('acceptMemberStatus:', err)
        throw err
      }
    },

  },
  getters: {
    acceptLocationHashMap: state => state.acceptLocationList.reduce((result, item) => {
      result[item.id] = item.name

      return result
    }, {}),
  },
})
