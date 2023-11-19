import { defineStore } from 'pinia'
import { removeToken, setToken } from '@/utils/auth'
import {
  reqEmailExists,
  reqForgotPassword,
  reqLogin,
  reqLogout,
  reqRegister,
  reqRequestVerifyToken,
  reqResetPassword,
  reqVerify,
} from '@/api/auth'
import { useToast } from 'vue-toastification'
import { useUserStore } from '@/stores/user'

const toast = useToast()

export const useAuthStore = defineStore({
  id: 'useAuthStore',
  actions: {
    async login({ username, password, remember }) {
      await reqLogin({ username, password })
        .then(async ({ data }) => {

          const userStore = useUserStore()

          userStore.$patch({ token: data.access_token })
          setToken(data.access_token)

          await this.$router.push({
            path: this.$router.currentRoute.value.query.redirect || '/',
          })

          toast.success(`歡迎 !`)

          if (remember) {
            localStorage.setItem('REMEMBER', '1')
            localStorage.setItem('EMAIL', username)
          } else {
            localStorage.removeItem('REMEMBER')
            localStorage.removeItem('EMAIL')
          }
        }).catch(() => {
          toast.error('登入失敗!')
        })
    },
    async logout() {
      await reqLogout().catch(() => {})
      removeToken()
      this.$patch({ token: '' })
      await this.$router.push({ name: 'Login' })
    },
    async register(payload) {
      await reqRegister(payload)
        .then(async () => {
          await this.$router.push({ name: 'Login' })
          toast.success('註冊成功!請前往電子信箱查看驗證信!')
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
    async resetPassword(payload) {
      await reqResetPassword(payload)
        .then(async () => {
          await this.$router.push({ name: 'Login' })
          toast.success('修改密碼成功')
        })
        .catch(async () => {
          toast.error('修改密碼失敗!請重新發送忘記密碼信!')
          await this.$router.push({ name: 'ForgotPassword' })
        })
    },
    async requestVerifyToken(payload) {
      await reqRequestVerifyToken(payload)
        .then(async () => {
          toast.success('請至輸入的信箱收取驗證信')
        })
        .catch(() => {
          toast.error('驗證信寄送失敗!')
        })
    },
    async verify(payload) {
      await reqVerify(payload)
        .then(async () => {
          await this.$router.push({ name: 'Login' })
          toast.success('信箱驗證成功!')
        })
        .catch(async () => {
          await this.$router.push({ name: 'RequestVerifyToken' })
          toast.error('驗證失敗! 請重新發送驗證信!')
        })
    },
    async emailExists(payload){
      await reqEmailExists(payload)

      // try {
      //
      //   return true
      // } catch {
      //   return false
      // }
    },
  },
})
