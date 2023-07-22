import axios from 'axios'
import urls from '@/api/urls'
import { app as vue } from '@/main'
import { useUserStore } from '@/stores/user'

const formDataList = [
  urls.auth.login,
]

export const request = axios.create()

request.interceptors.request.use(config => {
  console.log('vue', vue)
  console.log('$Progress', vue.config.globalProperties.$Progress)
  vue.config.globalProperties.$Progress.start()
  if (formDataList.includes(config.url)) {
    return {
      ...config,
      headers: {
        ...config.headers,
        accept: 'application/json',
        'Content-Type': 'multipart/form-data',
      },
    }
  }

  return config
}, error => Promise.reject(error))

request.interceptors.response.use(
  response => {
    vue.config.globalProperties.$Progress.finish()

    return response
  },
  error => {
    vue.config.globalProperties.$Progress.fail()

    console.log('request', error)

    // if (error.code === 'ECONNABORTED' && error.message && error.message.includes('timeout')) {
    //     alert('網路連線逾時')
    // } else {
    // alert('網路連線不穩定試')
    // }

    return Promise.reject(error)
  },
)

export const jwtRequest = axios.create()

jwtRequest.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    const result = {
      ...config,
      headers: {
        ...config.headers,
        Authorization: `Bearer ${userStore.token}`,
      },
    }

    if (formDataList.includes(config.url)) {
      result.headers['Content-Type'] = 'multipart/form-data'
    }

    return result
  }

  return config
}, error => Promise.reject(error))

jwtRequest.interceptors.response.use(response => {

  return response
}, error => {
  console.log('jwtRequest', error)
  if (error.response) {
    switch (error.response.status) {
    case 401:
      return Promise.reject(error)
    case 400:
      return Promise.reject(error)
    case 422:
      return Promise.reject(error)
    default:
      alert(`${error.response.status}: 未知。`)
      break
    }
  } else if (error.code === 'ECONNABORTED' && error.message && error.message.includes('timeout')) {
    alert('網路連線逾時')
  } else {
    alert('網路連線不穩定試')
  }

  return Promise.reject(error)
})

export const acceptRequest = axios.create()

acceptRequest.interceptors.request.use(config => {

  return {
    ...config,
    headers: {
      ...config.headers,
      Divergence: '1.048596',
    },
  }
}, error => Promise.reject(error))

acceptRequest.interceptors.response.use(
  response => {

    return response
  },
  error => {
    console.log('acceptRequest', error)

    return Promise.reject(error)
  },
)
