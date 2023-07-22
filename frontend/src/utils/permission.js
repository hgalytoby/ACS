import router from '@/router'
import { getToken } from '@/utils/auth'
import { useUserStore } from '@/stores/user'

const checkTokenSet = new Set(['ResetPassword', 'Verify'])
const authList = new Set(['Login', 'Register', 'ForgotPassword', 'ResetPassword', 'Verify'])
const whiteList = new Set(['Error404', 'NotAuthorized', 'UnderMaintenance', 'AuthCamera', 'OAuth', ...authList])

const checkQueryToken = (to, next) => {
  if (!to.query.token) {
    next({ name: 'NotAuthorized' })
  } else {
    next()
  }
}

router.beforeEach(async (to, from, next) => {
  document.title = `ACS ${to.meta.title}`

  const userStore = useUserStore()
  const hasToken = getToken()


  console.log(hasToken)
  if (hasToken) {
    if (authList.has(to.name)){
      next({ path: '/' })
    } else {
      const me = userStore.me

      if (me.id) {
        next()
      } else {
        try {
          await userStore.userInfo()
          next()
        } catch (error) {
          await userStore.resetToken()
          next(`/auth/login?redirect=${to.path}`)
        }
      }
    }
  } else if (whiteList.has(to.name)){
    if (checkTokenSet.has(to.name)) {
      checkQueryToken(to, next)
    } else {
      next()
    }
  } else {
    next(`/auth/login?redirect=${to.path}`)
  }
})
