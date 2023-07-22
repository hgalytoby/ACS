import { defineStore } from 'pinia'
import { reqUserInfo } from '@/api/user'
import { getToken, removeToken } from '@/utils/auth'

export const useUserStore = defineStore({
  id: 'useUserStore',
  state: () => ({
    token: getToken(),
    me: {},
  }),
  actions: {
    async userInfo() {
      await reqUserInfo().then(({ data }) => {
        this.$patch({ me: data })
      })
    },
    resetToken() {
      return new Promise(resolve => {
        removeToken()
        this.$patch({ token: '' })
        resolve()
      })
    },
  },
})
