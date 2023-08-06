import { defineStore } from 'pinia'
import { reqUpdatePassword, reqUpdateUserInfo, reqUserInfo, reqUserLog } from '@/api/user'
import { getToken, removeToken } from '@/utils/auth'
import { useToast } from 'vue-toastification'

const toast = useToast()

export const useUserStore = defineStore({
  id: 'useUserStore',
  state: () => ({
    token: getToken(),
    me: {
      'id': '',
      'email': '',
      'isActive': false,
      'isSuperuser': false,
      'isVerified': false,
      'username': '',
      'createdAt': '',
      'updatedAt': '',
      'avatar': '',
      'lastLogin': '',
      'roleIds': [],
    },
    log: {
      items: [],
      page: 1,
      pages: 1,
      size: 10,
      total: 1,
    },
  }),
  actions: {
    async userInfo() {
      await reqUserInfo().then(({ data }) => {
        this.$patch({ me: data })
      })
    },
    async updateUserInfo(payload) {
      await reqUpdateUserInfo(payload)
    },
    resetToken() {
      return new Promise(resolve => {
        removeToken()
        this.$patch({ token: '' })
        resolve()
      })
    },
    async updatePassword(payload) {
      await reqUpdatePassword(payload)
        .then(() => {
          toast.success('修改密碼成功!')
        }).catch(() => {
          toast.error('修改密碼失敗!')
        })
    },
    async userLog(params) {
      await reqUserLog(params).then(({ data }) => {
        data.items.forEach(item => item.rawData = JSON.stringify(item.rawData))
        this.$patch({ log: data })
      })
    },
  },
})
