import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    {
      path: '/',
      component: () => import('../layouts/default.vue'),
      children: [
        {
          path: 'dashboard',
          component: () => import('../pages/dashboard.vue'),
        },
        {
          path: 'account-settings',
          component: () => import('../pages/account-settings.vue'),
        },
        {
          path: 'typography',
          component: () => import('../pages/typography.vue'),
        },
        {
          path: 'icons',
          component: () => import('../pages/icons.vue'),
        },
        {
          path: 'cards',
          component: () => import('../pages/cards.vue'),
        },
        {
          path: 'tables',
          component: () => import('../pages/tables.vue'),
        },
        {
          path: 'form-layouts',
          component: () => import('../pages/form-layouts.vue'),
        },
      ],
    },
    {
      path: '/',
      component: () => import('../layouts/blank.vue'),
      children: [
        {
          path: 'login',
          component: () => import('../pages/login.vue'),
        },
        {
          path: 'register',
          component: () => import('../pages/register.vue'),
        },
        {
          path: '/:pathMatch(.*)*',
          component: () => import('../pages/[...all].vue'),
        },
        {
          path: 'auth',
          name: 'Auth',
          component: () => import('../pages/auth/index.vue'),
          redirect: '/auth/login',
          children: [
            {
              path: 'login',
              name: 'Login',
              component: () => import('../pages/auth/login.vue'),
              meta: {
                title: '登入',
              },
            },
            {
              path: 'register',
              name: 'Register',
              component: () => import('../pages/auth/register.vue'),
              meta: {
                title: '註冊',
              },
            },
            {
              path: 'forgot-password',
              name: 'ForgotPassword',
              component: () => import('../pages/auth/forgot_password.vue'),
              meta: {
                title: '忘記密碼',
              },
            },
          ],
        },
      ],
    },
  ],
})

export default router
