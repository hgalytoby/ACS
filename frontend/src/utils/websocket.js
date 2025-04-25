import ReconnectingWebSocket from 'reconnecting-websocket'
import { useUserStore } from '@/stores/user'
import { useMemberStore } from '@/stores/member'

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
  const payload = JSON.parse(event.data)
  const memberStore = useMemberStore()

  if (payload.event === 'LOGIN' && payload.data.success) {
    sendWebSocketMessage({
      event: 'MEMBER_STATUS_LIST',
    })
  } else if (payload.event === 'MEMBER_STATUS_LIST') {
    console.log('MEMBER_STATUS_LIST', payload.data)
    memberStore.updateStatusList(payload.data)
  } else if (payload.event === 'MEMBER_STATUS') {
    console.log('MEMBER_STATUS', payload.data)
  }
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

