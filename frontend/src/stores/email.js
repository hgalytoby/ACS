import { defineStore } from 'pinia'
import { reqEmailSetting, reqEmailSettingsList, reqEmailSettingsUpdate, reqEmailTrySend } from '@/api/email'
import { useToast } from 'vue-toastification'

const toast = useToast()

export const useEmailStore = defineStore({
  id: 'useEmailStore',
  state: () => ({
    UserRegister: {},
    UserForgotPassword: {},
    UserResetPassword: {},
    UserVerify: {},
    UserDestroy: {},
    UserLoginFail: {},
  }),
  actions: {
    async settingList() {
      await reqEmailSettingsList().then(({ data }) => {
        data.forEach(item => this.$patch({ [item.event]: item }))
      })
    },
    async setting(event) {
      await reqEmailSetting(event).then(({ data }) => {
        this.$patch({ [event]: data })
      })
    },
    async settingUpdate(payload) {
      await reqEmailSettingsUpdate(payload)
        .then(() => {
          toast.success('更新成功!')
        }).catch(() => {
          toast.error('更新失敗!')
        })
    },
    async settingTrySend(payload) {
      await reqEmailTrySend(payload)
        .then(() => {
          toast.success('發送成功!')
        }).catch(() => {
          toast.error('發送失敗!')
        })
    },
  },
})
