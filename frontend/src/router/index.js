import { createRouter as _createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

const createRouter = () => new _createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

const router = createRouter()
export default router
