import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

const reqLogUsers = params => jwtRequest.get(urls.log.users, { params })

const reqLogSystems = params => jwtRequest.get(urls.log.systems, { params })

const reqLogSystem = systemId => jwtRequest.get(urls.log.system(systemId))
