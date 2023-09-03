import { defineStore } from 'pinia'
import {
  reqOAuthAuthorize,
  reqOAuthCallback,
  reqOAuthAssociateAuthorize,
  reqOAuthAssociateCallback,
} from '@/api/oauth'
import { setToken } from '@/utils/auth'
import { useUserStore } from '@/stores/user'
import { useToast } from 'vue-toastification'

const toast = useToast()

export const useOAuthStore = defineStore({
  id: 'useOAuthStore',
  actions: {
    async authorize(payload) {
      await reqOAuthAuthorize(payload)
        .then(({ data }) => {
          // console.log(data.authorization_url)
          window.location.href = data.authorization_url
        })
    },
    async callback({ providerName, query }) {
      await reqOAuthCallback(providerName, query)
        .then(async ({ data }) => {
          const userStore = useUserStore()

          userStore.$patch({ token: data.access_token })
          setToken(data.access_token)
          await this.$router.push('/')
        })
    },

    async associateAuthorize(payload) {
      await reqOAuthAssociateAuthorize(payload)
        .then(({ data }) => {
          window.location.href = data.authorization_url
        })
    },
    async associateCallback({ providerName, query }) {
      await reqOAuthAssociateCallback(providerName, query)
        .then(async () => {
          const userStore = useUserStore()

          await userStore.me()
          this.$router.push({ name: 'AccountSettings' })
          toast.success(`綁定 ${providerName} 帳號成功!`)
        }).catch(() => {
          toast.error(`綁定 ${providerName} 帳號失敗!`)
        })
    },
  },
})
