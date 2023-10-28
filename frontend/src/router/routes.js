export default [
  { path: '/', redirect: '/account-settings' },
  {
    path: '/',
    component: () => import('../layouts/default.vue'),
    children: [
      {
        path: 'dashboard',
        component: () => import('../pages/dashboard.vue'),
        meta: {
          title: '儀錶板',
        },
      },
      {
        path: 'account-settings',
        name: 'AccountSettings',
        component: () => import('../pages/account-settings/index.vue'),
        meta: {
          title: '帳號設定',
        },
      },
      {
        path: 'user-list',
        name: 'UserList',
        component: () => import('../pages/settings/user-list.vue'),
        meta: {
          title: '使用者列表',
        },
      },
      {
        path: 'user-log',
        name: 'UserLog',
        component: () => import('../pages/settings/user-log.vue'),
        meta: {
          title: '使用者日誌',
        },
      },
      {
        path: 'email-log',
        name: 'EmailLog',
        component: () => import('../pages/settings/email-log.vue'),
        meta: {
          title: '信箱日誌',
        },
      },
      {
        path: 'email-message',
        name: 'EmailMessage',
        component: () => import('../pages/settings/email-message.vue'),
        meta: {
          title: '信箱訊息',
        },
      },
      {
        path: 'member-location-list',
        name: 'MemberLocationList',
        component: () => import('../pages/settings/member-location-list.vue'),
        meta: {
          title: '成員地點列表',
        },
      },
      {
        path: 'locations-overview',
        name: 'LocationOverview',
        component: () => import('../pages/locations-overview.vue'),
        meta: {
          title: '地點概覽',
        },
      },
      {
        path: 'member-list',
        name: 'MemberList',
        component: () => import('../pages/member/list.vue'),
        meta: {
          title: '成員列表',
        },
      },
      {
        path: 'member-create',
        name: 'MemberCreate',
        component: () => import('../pages/member/create.vue'),
        meta: {
          title: '新增成員',
        },
      },
      {
        path: 'member-record-list',
        name: 'MemberRecordList',
        component: () => import('../pages/member/record-list.vue'),
        meta: {
          title: '成員紀錄列表',
        },
      },
      {
        path: 'camera',
        name: 'Camera',
        component: () => import('../pages/camera.vue'),
        meta: {
          title: 'Camera',
        },
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
            name: 'AuthCamera',
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
          title: '第三方綁定驗證',
        },
      },
    ],
  },
]
