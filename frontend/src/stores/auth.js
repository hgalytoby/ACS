import { defineStore } from 'pinia'
import { getToken, removeToken, setToken } from '@/utils/auth'
import { reqForgotPassword, reqLogin, reqLogout, reqRegister } from '@/api/auth'
import { useToast } from "vue-toastification"

const toast = useToast()
export const useAuthStore = defineStore({
  id: 'useAuthStore',
  state: () => ({
    token: getToken(),
  }),

  actions: {
    async login({ username, password, remember }) {
      await reqLogin({ username, password })
        .then(async ({ data }) => {
          toast.success('登入成功!')
          setToken(data)
          this.$patch({ token: data })
          if (remember) {
            localStorage.setItem('REMEMBER', '1')
            localStorage.setItem('EMAIL', username)
          } else {
            localStorage.removeItem('REMEMBER')
            localStorage.removeItem('EMAIL')
          }
          await this.$router.push('/')
        }).catch(() => {
          toast.error('登入失敗!')
        })
    },
    async logout() {
      await reqLogout()
      removeToken()
      this.$patch({ token: '' })
    },
    async register(payload) {
      await reqRegister(payload)
        .then(async () => {
          toast.success('註冊成功!請前往電子信箱查看驗證信!')
          await this.$router.push({ name: 'Login' })
        })
        .catch(() => {
          toast.error('註冊失敗!')
        })
    },
    async forgotPassword(payload) {
      await reqForgotPassword(payload)
        .then(async () => {
          toast.success('前往電子信箱查看驗證信!')
        })
        .catch(() => {
          toast.error('寄送驗證信失敗!')
        })
    },
  },
})
