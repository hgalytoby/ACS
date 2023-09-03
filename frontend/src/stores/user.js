import { defineStore } from 'pinia'
import {
  reqUnlinkOAuthAccount,
  reqUpdateMePassword,
  reqUpdateMeInfo,
  reqMe,
  reqUserLog,
  reqUserList,
  reqUserInfo,
} from '@/api/user'
import { getToken, removeToken } from '@/utils/auth'
import { useToast } from 'vue-toastification'

const toast = useToast()

const getDefaultUserInfo = () => {
  return {
    id: '',
    email: '',
    isActive: false,
    isSuperuser: false,
    isVerified: false,
    username: '',
    createdAt: '',
    updatedAt: '',
    avatar: '',
    roleList: [],
    oauthAccounts: [],
  }
}

export const useUserStore = defineStore({
  id: 'useUserStore',
  state: () => ({
    token: getToken(),
    meInfo: getDefaultUserInfo(),
    log: {
      items: [],
      pages: 1,
      total: 1,
    },
    list: {
      items: [],
      pages: 1,
      total: 1,
    },
    user: getDefaultUserInfo(),
  }),
  actions: {
    async me() {
      await reqMe()
        .then(({ data }) => {
          this.$patch({ meInfo: data })
        })
    },
    async updateMeInfo(payload) {
      await reqUpdateMeInfo(payload)
      toast.success('修改基本資料成功!')
    },
    resetToken() {
      return new Promise(resolve => {
        removeToken()
        this.$patch({ token: '' })
        resolve()
      })
    },
    async updateMePassword(payload) {
      await reqUpdateMePassword(payload)
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
    async userList(params) {
      await reqUserList(params)
        .then(({ data }) => {
          this.$patch({ list: data })
        })
    },
    async unlinkOauthAccount(providerName) {
      await reqUnlinkOAuthAccount({ providerName })
        .then(async () => {
          await this.me()
          toast.success(`解除 ${providerName} 綁定!`)
        })
    },
    async userInfo(payload) {
      await reqUserInfo(payload).then(({ data }) => {
        this.$patch({ user: data })
      })
    },
    async resetUserInfo() {
      this.$patch({ 
        user: {
          id: '',
          email: '',
          isActive: false,
          isSuperuser: false,
          isVerified: false,
          username: '',
          createdAt: '',
          updatedAt: '',
          avatar: '',
          roleList: [],
          oauthAccounts: [],
        }, 
      })
    },
  },
})
