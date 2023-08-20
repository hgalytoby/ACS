import urls from '@/api/urls'
import { acceptRequest } from '@/utils/requests'

export const reqAcceptLocation = () => acceptRequest.get(urls.accept.acceptLocation)

export const reqAcceptApi = () => acceptRequest.get(urls.accept.acceptApi)
