import Vue from "vue";

/*** 长文本溢出省略**/
function get_content(the_content, low, high) {
  let content = the_content.slice(low, high)
  if (the_content.length > 10) {
    content += '...'
  }
  return content
}

/**检查是否登录**/
function check_user_login() {
  let token = localStorage.token || sessionStorage.token;
  if (!token) {
    let self = this;
    this.$alert("登录失效", {
      callback() {
        self.$router.push("/login");
      }
    });
    return false
  }
  return token;
}

/**强制登录**/
function force_login() {
  let token = localStorage.token || sessionStorage.token;
  if (!token) {
    let self = this
    this.$alert("未登录或登录失效,请先登录", {
      callback() {
        self.$router.push('/login')
      }
    })
  }


}

export {
  get_content,
  check_user_login,
  force_login
}


