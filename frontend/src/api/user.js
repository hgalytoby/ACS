import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqUserInfo = () => jwtRequest.get(urls.user.me)
