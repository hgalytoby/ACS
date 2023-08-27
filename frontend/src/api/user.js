import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqUserInfo = () => jwtRequest.get(urls.user.me)

export const reqUpdatePassword = payload => jwtRequest.patch(urls.user.updatePassword, payload)

export const reqUpdateUserInfo = payload => jwtRequest.patch(urls.user.updateUserInfo, payload)

export const reqUserLog = params => jwtRequest.get(urls.user.log, { params })

export const reqUserList = params => jwtRequest.get(urls.user.list, { params })

export const reqUnlinkOAuthAccount = params => jwtRequest.delete(urls.user.unlinkOAuth, { params })
