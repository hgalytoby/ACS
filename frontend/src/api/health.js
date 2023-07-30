import { request } from '@/utils/requests'
import urls from '@/api/urls'

export const reqHealth = () => request.get(urls.healthAPI)
