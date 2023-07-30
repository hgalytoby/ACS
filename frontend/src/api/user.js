import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqUserInfo = () => jwtRequest.get(urls.user.me)

export const reqUpdatePassword = payload => jwtRequest.patch(urls.user.updatePassword, payload)

export const reqUpdateUserInfo = payload => jwtRequest.patch(urls.user.updateUserInfo, payload)
export const reqUserLog = () => jwtRequest.get(urls.user.log)

