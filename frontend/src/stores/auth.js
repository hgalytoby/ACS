import {defineStore} from 'pinia'
import {getToken, removeToken, setToken} from '@/utils/auth'
import {reqLogin, reqLogout} from '@/api/auth'

export const useAuthStore = defineStore({
    id: 'useAuthStore',
    state: () => ({
        token: getToken(),
    }),

    actions: {
        async login(payload) {
            await reqLogin(payload).then(({data}) => {
                setToken(data)
                this.$patch({token: data})
            })
        },
        async logout() {
            await reqLogout()
            removeToken()
            this.$patch({token: ''})
        },
    },
})
