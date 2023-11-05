import ReconnectingWebSocket from 'reconnecting-websocket'
import { useUserStore } from '@/stores/user'

const protocol = window.location.protocol === 'http:' ? 'ws' : 'wss'

const url = process.env.NODE_ENV === 'production' ? `${protocol}://${window.location.host}/ws` : `${protocol}://localhost:8000/ws`

let webSocket

export const sendWebSocketMessage = msg => {
  console.log('sendWebSocketMessage', msg)
  if (webSocket.readyState === 1) webSocket.send(JSON.stringify(msg))
}

export const webLogin = () => {
  const userStore = useUserStore()

  sendWebSocketMessage({
    event: 'LOGIN',
    data: userStore.token,
  })
}

function connect() {
  webLogin()
}

function message(event) {
  const data = JSON.parse(event.data)

  console.log(data)

  // if (data.event === 'login' && data.success) {
  //   sendWebSocketMessage({
  //     action: 'member_come_list',
  //   })
  // } else if (data.action === 'member_come_list') {
  //   console.log('member_come_list', data.items)
  //   store.commit('member/SET_MEMBER_COME_LIST', data.items)
  // } else if (data.action === 'member_come') {
  //   console.log('member_come', data.items)
  //   store.commit('member/SET_MEMBER_COME_INFO_LIST', data.items)
  //
  // }
}

function close(event) {
  console.log(event, 'close ok')
}

function error(event) {
  console.log(event, 'error ok')
}

export const closeSocketMessage = () => {
  if (webSocket && webSocket.readyState === WebSocket.OPEN) {
    webSocket.close()
  }
}

export const connectWebSocket = () => {
  webSocket = new ReconnectingWebSocket(url)
  webSocket.addEventListener('open', connect)
  webSocket.addEventListener('message', message)
  webSocket.addEventListener('close', close)
  webSocket.addEventListener('error', error)
}

