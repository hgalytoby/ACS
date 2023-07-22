import { defineStore } from 'pinia'
import { reqOAuthAuthorize, reqOAuthCallback } from '@/api/oauth'
import { setToken } from '@/utils/auth'
import { useUserStore } from '@/stores/user'

export const useOAuthStore = defineStore({
  id: 'useOAuthStore',
  actions: {
    async authorize(payload) {
      if (!this.oauth?.[payload]) {
        await reqOAuthAuthorize(payload).then(({ data }) => {
          this.$patch({
            [payload]: data.authorization_url,
          })
          window.location.href = data.authorization_url
        })
      } else {
        window.location.href = this.oauth[payload]
      }
    },
    async callback({ name, query }) {
      await reqOAuthCallback(name, query).then(async ({ data }) => {
        const userStore = useUserStore()

        userStore.$patch({ token: data.access_token })
        setToken(data.access_token)
        await this.$router.push('/')
      })
    },
    async associateAuthorize(payload) {

    },
    async associateCallback(name, payload) {

    },
  },
})
