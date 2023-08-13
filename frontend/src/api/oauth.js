import { jwtRequest, request } from '@/utils/requests'
import urls from '@/api/urls'

export const reqOAuthAuthorize = payload => request.get(
  urls.oauth.authorize(payload),
  { 
    params: {
      redirect_url: `${window.location.origin}/oauth/${payload}/callback`,
    },
  },
)
export const reqOAuthCallback = (providerName, payload) => request.get(
  urls.oauth.callback(providerName),
  { 
    params: {
      redirect_url: `${window.location.origin}/oauth/${providerName}/callback`,
      ...payload,
    },
  },
)
export const reqOAuthAssociateAuthorize = payload => jwtRequest.get(
  urls.oauth.associateAuthorize(payload),
  {
    params: {
      redirect_url: `${window.location.origin}/oauth/associate/${payload}/callback`,
    },
  },
)
export const reqOAuthAssociateCallback = (providerName, payload) => jwtRequest.get(
  urls.oauth.associateCallback(providerName),
  {
    params: {
      redirect_url: `${window.location.origin}/oauth/associate/${providerName}/callback`,
      ...payload,
    },
  },
)
