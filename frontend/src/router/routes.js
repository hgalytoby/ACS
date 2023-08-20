export default [
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
        path: 'account-settings/:tab?',
        name: 'AccountSettings',
        component: () => import('../pages/account-settings/index.vue'),
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
        path: '/:pathMatch(.*)*',
        component: () => import('../pages/[...all].vue'),
      },
      {
        path: '/not-authorized',
        name: 'NotAuthorized',
        component: () => import('../pages/other/not-authorized.vue'),
        meta: {
          layout: 'blank',
          title: '權限不足',
        },
      },
      {
        path: '/under-maintenance',
        name: 'UnderMaintenance',
        component: () => import('../pages/other/under-maintenance.vue'),
        meta: {
          layout: 'blank',
          title: '維修中',
        },
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
              title: '註冊帳號',
            },
          },
          {
            path: 'forgot-password',
            name: 'ForgotPassword',
            component: () => import('../pages/auth/forgot-password.vue'),
            meta: {
              title: '忘記密碼',
            },
          },
          {
            path: 'reset-password',
            name: 'ResetPassword',
            component: () => import('../pages/auth/reset-password.vue'),
            meta: {
              title: '重設密碼',
            },
          },
          {
            path: 'request-verify-token',
            name: 'RequestVerifyToken',
            component: () => import('../pages/auth/request-verify-token.vue'),
            meta: {
              title: '請求啟用信箱驗證信',
            },
          },
          {
            path: 'verify',
            name: 'Verify',
            component: () => import('../pages/auth/verify.vue'),
            meta: {
              title: '啟用驗證',
            },
          },
          {
            path: 'camera',
            name: 'Camera',
            component: () => import('../pages/auth/camera.vue'),
            meta: {
              title: 'QRCode',
            },
          },
        ],
      },
      {
        path: '/oauth/:providerName/callback',
        name: 'OAuth',
        component: () => import('../pages/oauth/oauth.vue'),
        meta: {
          layout: 'blank',
          title: '第三方驗證',
        },
      },
      {
        path: '/oauth/associate/:providerName/callback',
        name: 'OAuthAssociate',
        component: () => import('../pages/oauth/oauth-associate.vue'),
        meta: {
          layout: 'blank',
          title: '第三方綁定讞正',
        },
      },
    ],
  },
]
