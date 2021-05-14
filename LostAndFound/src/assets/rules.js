/** 验证是否是正确的手机号格式**/
export function checkPhone(rule,value,callback) {
  if(!/^1[3-9]\d{9}$/.test(value)){
    callback(new Error('请输入正确的手机号'))
  }
  else {
    callback()
  }
}


