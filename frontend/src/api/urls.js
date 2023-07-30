import { reqEmailExists } from '@/api/auth'

const auth = {
  login: '/api/v1/auth/jwt/login',
  logout: '/api/v1/auth/jwt//logout',
  register: '/api/v1/auth/register',
  forgotPassword: '/api/v1/auth/forgot-password',
  resetPassword: '/api/v1/auth/reset-password',
  requestVerifyToken: '/api/v1/auth/request-verify-token',
  verify: '/api/v1/auth/verify',
  emailExists: '/api/v1/users/email-exists',
}

const oauth = {
  authorize: name => `/api/auth/${name}/authorize`,
  callback: name =>`/api/auth/${name}/callback`,
  associateAuthorize: name =>`/api/auth/associate/${name}/authorize`,
  associateCallback: name => `/api/auth/associate/${name}/authorize`,
}

const user = {
  me: '/api/v1/users/me',
  updateUserInfo: '/api/v1/users/me/info',
  updatePassword: '/api/v1/users/me/update-password',
  log: '/api/v1/users/me/log',
  info: '/api/v1/users/me/info',
}

const healthAPI = '/api/health'

export default {
  auth,
  oauth,
  user,
  healthAPI,
}
