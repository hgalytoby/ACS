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
export const reqOAuthCallback = (name, payload) => request.get(
  urls.oauth.callback(name),
  { 
    params: {
      redirect_url: `${window.location.origin}/oauth/${name}/callback`,
      ...payload,
    },
  },
)
export const reqOAuthAssociateAuthorize = payload => request.get(
  urls.oauth.associateAuthorize(payload),
)
export const reqOAuthAssociateCallback = (name, payload) => request.get(
  urls.oauth.associateCallback(payload),
  { 
    params: payload,
  },
)
