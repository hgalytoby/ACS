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
  authorize: providerName => `/api/auth/${providerName}/authorize`,
  callback: providerName => `/api/auth/${providerName}/callback`,
  associateAuthorize: providerName => `/api/auth/associate/${providerName}/authorize`,
  associateCallback: providerName => `/api/auth/associate/${providerName}/callback`,
}

const user = {
  me: '/api/v1/users/me',
  updateUserInfo: '/api/v1/users/me/info',
  updatePassword: '/api/v1/users/me/update-password',
  log: '/api/v1/users/me/log',
  info: '/api/v1/users/me/info',
  unlinkOAuth: '/api/v1/users/me/unlink-oauth',
}

const member = {
  members: '/api/v1/members',
  member: id => `/api/v1/members/${id}`,
  membersRecord: '/api/v1/members-record',
  memberRecord: id => `/api/v1/members-record/${id}`,
  memberStatus: '/api/v1/member-status',
  membersLocation: '/api/v1/members-location',
  memberLocation: id => `/api/v1/members-location/${id}`,
}

const accept = {
  acceptLocation: '/api/accept-location',
  acceptApi: '/api/accept-api',
}

const healthAPI = '/api/health'

export default {
  auth,
  oauth,
  user,
  healthAPI,
  member,
  accept,
}
