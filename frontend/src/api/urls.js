const auth = {
  login: '/api/v1/auth/login',
  logout: '/api/v1/auth/logout',
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
  updateMeInfo: '/api/v1/users/me/info',
  updateMePassword: '/api/v1/users/me/update-password',
  log: '/api/v1/users/me/log',
  info: '/api/v1/users/me/info',
  unlinkOAuth: '/api/v1/users/me/unlink-oauth',
  list: '/api/v1/users',
  user: id => `/api/v1/users/${id}`,
}

const member = {
  members: '/api/v1/members',
  member: id => `/api/v1/members/${id}`,
  membersRecord: '/api/v1/members-record',
  memberRecord: id => `/api/v1/members-record/${id}`,
  membersLocation: '/api/v1/members-location',
  memberLocation: id => `/api/v1/members-location/${id}`,
}

const accept = {
  acceptLocation: '/api/accept-location',
  acceptApi: '/api/accept-api',
  acceptMemberStatus: '/api/accept-member-status',
}

const log = {
  users: '/api/v1/log/users',
  systems: '/api/v1/log/systems',
  system: id => `/api/v1/log/systems/${id}`,
}

const healthAPI = '/api/health'

const chart = {
  hardDiskVolume: '/api/v1/charts/hard-disk-volume',
  emailLogClassification: '/api/v1/charts/email-log-classification',
  memberGrowth: '/api/v1/charts/member-growth',
  newMemberChart: '/api/v1/charts/new-member-chart',
  memberRecordGrowth: '/api/v1/charts/member-record-growth',
  memberRecordHourlyCount: '/api/v1/charts/member-record-hourly-count',
  allChart: '/api/v1/charts/all-chart',
}

const email = {
  settings: '/api/v1/email-settings',
  setting: id => `/api/v1/email-settings/${id}`,
  trySend: '/api/v1/email-try-send',
}

export default {
  auth,
  oauth,
  user,
  healthAPI,
  member,
  accept,
  log,
  chart,
  email,
}
