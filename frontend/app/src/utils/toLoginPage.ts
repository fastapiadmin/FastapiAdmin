// 跳转到登录页
export function toLoginPage(
  options: { mode?: 'navigateTo' | 'reLaunch' } = {},
) {
  const { mode = 'navigateTo' } = options

  if (mode === 'reLaunch') {
    uni.reLaunch({
      url: '/pages/login/index',
    })
  }
  else {
    uni.navigateTo({
      url: '/pages/login/index',
    })
  }
}
