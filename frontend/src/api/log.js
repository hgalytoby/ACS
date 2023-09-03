import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqLogUsers = params => jwtRequest.get(urls.log.users, { params })

export const reqLogSystems = params => jwtRequest.get(urls.log.systems, { params })

export const reqLogSystem = systemId => jwtRequest.get(urls.log.system(systemId))
