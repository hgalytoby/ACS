export const userLogSelectItem = [
  { name: '請選擇動作', value: null },
  { name: '新增成員', value: 'CreateMember' },
  { name: '更新成員', value: 'UpdateMember' },
  { name: '刪除成員', value: 'DestroyMember' },
  { name: '新增地點', value: 'CreateMemberLocation' },
  { name: '更新地點', value: 'UpdateMemberLocation' },
  { name: '刪除地點', value: 'DestroyMemberLocation' },
  { name: '使用者登入', value: 'LoginUser' },
  { name: '啟用使用者', value: 'VerifyUser' },
  { name: '更新使用者', value: 'UpdateUser' },
  { name: '刪除使用者', value: 'DestroyUser' },
]

export const bloodTypeSelectItem = [
  { name: '請選擇血型', value: null },
  { name: 'A', value: 'A' },
  { name: 'B', value: 'B' },
  { name: 'AB', value: 'AB' },
  { name: 'O', value: 'O' },
]

export const statusSelectItem = [
  { name: '請選擇進出入狀態', value: null },
  { name: '進入', value: true },
  { name: '離開', value: false },
]

export const systemLogSelectItem = [
  { name: '請選擇動作', value: null },
  { name: '使用者註冊', value: 'UserRegister' },
  { name: '使用者登入失敗', value: 'UserLoginFail' },
  { name: '使用者忘記密碼', value: 'UserForgotPassword' },
  { name: '使用者重置密碼', value: 'UserResetPassword' },
  { name: '驗證使用者', value: 'UserVerify' },
  { name: '刪除使用者', value: 'UserDestroy' },
  { name: '測試送信', value: 'TrySendEmail' },
]
