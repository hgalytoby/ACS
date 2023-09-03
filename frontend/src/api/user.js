import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqMe = () => jwtRequest.get(urls.user.me)

export const reqUpdateMePassword = payload => jwtRequest.patch(urls.user.updateMePassword, payload)

export const reqUpdateMeInfo = payload => jwtRequest.patch(urls.user.updateMeInfo, payload)

export const reqUserLog = params => jwtRequest.get(urls.user.log, { params })

export const reqUserList = params => jwtRequest.get(urls.user.list, { params })

export const reqUnlinkOAuthAccount = params => jwtRequest.delete(urls.user.unlinkOAuth, { params })

export const reqUserInfo = userId => jwtRequest.get(urls.user.user(userId))

