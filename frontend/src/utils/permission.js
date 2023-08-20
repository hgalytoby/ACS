import router from '@/router'
import { getToken } from '@/utils/auth'
import { useUserStore } from '@/stores/user'
import { authProviderItems } from '@/utils/oauth'
import { useHealthStore } from '@/stores/health'

const checkTokenSet = new Set(['ResetPassword', 'Verify'])
const authSet = new Set(['Login', 'Register', 'ForgotPassword', 'ResetPassword', 'Verify', 'OAuth', 'Camera', 'Camera2'])
const whiteSet = new Set(['Error404', 'NotAuthorized', 'UnderMaintenance', 'AuthCamera', 'OAuth', ...authSet])

const checkQueryToken = (to, next) => {
  if (!to.query.token) {
    next({ name: 'NotAuthorized' })
  } else {
    next()
  }
}

const checkOAuthName = (to, next) => {
  if (to.params.providerName in authProviderItems) {
    next()
  } else {
    next({ name: 'NotAuthorized' })
  }
}

const redirectToLogin = (to, next) => {
  next(`/auth/login?redirect=${to.path}`)
}

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title

  const healthStore = useHealthStore()
  const userStore = useUserStore()
  const hasToken = getToken()

  if (to.name === 'UnderMaintenance') {
    try {
      await healthStore.health()
      next('/')
    } catch (error) {
      next()
    }
    
    return
  }

  // 在需要確認健康狀態的頁面，確保已獲取健康狀態
  if (!healthStore.project) {
    try {
      await healthStore.health()
    } catch (error) {
      next({ name: 'UnderMaintenance' })
      
      return
    }
  }
  document.title = `${healthStore.project} ${to.meta.title}`

  if (hasToken) {
    // 已經登錄的情況
    if (authSet.has(to.name)) {
      // 已經登錄的頁面
      next({ path: '/' })
    } else {
      // 非登錄頁面，確保有用戶信息
      const me = userStore.me
      if (me.id) {
        next()
      } else {
        try {
          await userStore.userInfo()
          next()
        } catch (error) {
          // 用戶信息獲取失敗，重置 token 並跳轉到登錄頁面
          await userStore.resetToken()
          redirectToLogin(to, next)
        }
      }
    }
  } else if (whiteSet.has(to.name)) {
    // 未登錄且在白名單中的頁面
    if (to.name === 'OAuth') {
      checkOAuthName(to, next)
    } else if (checkTokenSet.has(to.name)) {
      checkQueryToken(to, next)
    } else {
      next()
    }
  } else {
    // 未登錄，不在白名單中的頁面，跳轉到登錄頁面
    redirectToLogin(to, next)
  }
})
