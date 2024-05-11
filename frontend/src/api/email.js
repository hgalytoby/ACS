import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqEmailSettingsList = () => jwtRequest.get(urls.email.settings)
export const reqEmailSettingsUpdate = payload => jwtRequest.patch(urls.email.setting(payload.event), payload)
export const reqEmailTrySend = payload => jwtRequest.post(urls.email.trySend, payload)
