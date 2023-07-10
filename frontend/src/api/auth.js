import {jwtRequest, request} from '@/utils/requests'
import urls from '@/api/urls'


export const reqLogin = payload => request.post(urls.auth.login, payload)

export const reqLogout = () => jwtRequest.post(urls.auth.logout)

export const reqRegister = payload => request.post(urls.auth.register, payload)

export const reqForgotPassword = payload => request.post(urls.auth.forgotPassword, payload)

export const reqResetPassword = payload => request.post(urls.auth.resetPassword, payload)

export const reqRequestVerifyToken = payload => request.post(urls.auth.requestVerifyToken, payload)

export const reqVerify = payload => request.post(urls.auth.verify, payload)
