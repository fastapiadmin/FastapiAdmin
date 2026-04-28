/**
 * 表情
 * 用于在消息提示的时候显示对应的表情
 *
 * 用法
 * ElMessage.success(`${EmojiText[200]} 图片上传成功`)
 * ElMessage.error(`${EmojiText[400]} 图片上传失败`)
 * ElMessage.error(`${EmojiText[500]} 图片上传失败`)
 *
 * @module utils/ui/emojo
 * @author Fastapi Admin Team
 */

// macos 用户 按 shift + 6 可以唤出更多表情……
const EmojiText: { [key: string]: string } = {
  '0': 'O_O', // 空
  '200': '^_^', // 成功
  '400': 'T_T', // 错误请求
  '500': 'X_X', // 服务器内部错误，无法完成请求
};

// const EmojiIcon = ['🟢', '🔴', '🟡 ', '🚀', '✨', '💡', '🛠️', '🔥', '🎉', '🌟', '🌈']

export default EmojiText;
