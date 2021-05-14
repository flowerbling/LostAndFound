<template>
  <div class="login box">
    <img src="/static/image/bg.png" alt="">
    <div class="login">
      <div class="login-title">
        <a href="/"><img src="/static/image/logo.png" alt="花朵闪闪-花卉中心"></a>
        <p>丢了东西不要怕，寻物局帮你找到它！</p>
      </div>
      <div class="login_box">
        <div class="title">
          <span @click="log_with_psw" :style=style_psw>密码登录</span>
          <span @click="log_with_msg" :style=style_msg>短信登录</span>
        </div>
        <div class="inp" v-if="use_psw">
          <label>
            <input type="text" placeholder="用户名 / 手机号码" class="user" v-model="username">
          </label>
          <label>
            <input type="password" name="" class="pwd" placeholder="密码" v-model="password">
          </label>
          <div id="show_captcha"></div>
          <div class="rember">
            <p>
              <label>
                <input type="checkbox" class="no" v-model="remember_me"/>
              </label>
              <span>记住密码</span>
            </p>
            <p>忘记密码</p>
          </div>
          <button class="login_btn btn btn-primary" @click="get_captcha">登录</button>
          <p class="go_login">没有账号
            <router-link to="/register/">立即注册</router-link>
          </p>
        </div>
        <div class="inp" v-else>
          <input type="text" placeholder="手机号码" class="user" @blur="check_phone" v-model="phone">
          <div class="sms-box"><input type="text" class="pwd" placeholder="短信验证码" @blur="check_code"
                                      v-model="code">
            <div class="sms-btn" @click="get_code" v-if="show">发送验证码</div>
            <div class="sms-btn" v-else>已发送 {{ left_time }}</div>
          </div>
          <button class="login_btn" @click="phone_login">登录</button>
          <br>
          <br>
          <span class="go_login">没有账号
                     <router-link to="/register/">立即注册</router-link>
                </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      code: '',
      remember_me: false,
      use_psw: true,
      phone: "",
      phone_true: false,
      code_true: false,
      left_time: '',
      the_set: '',
      show: true,
      style_psw:' border-bottom: 2px solid #2d8da3;',
      style_msg:'',
    }
  },
  methods: {

    // 验证验证码
    check_code() {
      if (this.code.length !== 6) {
        this.code_true = false
        // this.$message.error('请输入正确的验证码')
        return false
      } else {
        this.code_true = true;
      }

    },
    // 手机登录
    phone_login() {
      if (!this.phone_true) {
        this.$message.error("手机号未注册或手机号错误")
        return false;
      }
      this.$axios({
        url: this.$settings.HOST + 'user/phone_login/',
        method: 'get',
        params: {
          phone: this.phone,
          code: this.code
        },
      }).then(res => {
        if (res.data) {
          // 将token信息保存
          sessionStorage.token = res.data.token;
          sessionStorage.user = res.data.user;
          sessionStorage.user_id = res.data.user_id;
          sessionStorage.user_head = res.data.user_head;
          this.$message({
            message: "恭喜你，登陆成功",
            type: "success",
            duration: 1000,
          })
        }
        // 登陆成功后返回到首页
        this.$router.push("/")
      }).catch(error => {
        this.$message.error(error.response.data)
      })
    },
    // 检查手机号是否被注册
    check_phone() {
      if(this.phone.length !== 11 || !/1[345678][0-9]{9}/.test(this.phone)){
        this.$message.error("请输入正确的手机号")
        return false
      }
      let self = this
      this.$axios({
        url: this.$settings.HOST + "user/phone_check/",
        method: "get",
        params: {
          phone: this.phone,
        }
      }).then(res => {
          self.phone_true = true
        }
      ).catch(error => {
        this.$message.error(error.response.data)
        self.phone_true = false
      })
    },
    //计时程序
    count_time() {
      this.left_time -= 1
      if (this.left_time <= 0) {
        clearInterval(this.the_set);
        this.show = true
        this.left_time = '';
      }
    },


    // 根据手机号获取验证码
    get_code() {
      if (!this.phone_true) {
        this.$message.error("手机号未注册或手机号错误")
        return false
      }
      this.$message.success("验证码发送成功,请注意查收")
      this.left_time = 60
      this.show = false
      this.the_set = setInterval(this.count_time, 1000)
      this.$axios({
        url: this.$settings.HOST + "user/send/",
        method: "get",
        params: {
          phone: this.phone
        }
      }).then(res => {
        console.log(res);
      }).catch(error => {
        this.$message.error(error.respond.data)
      })
    },
    log_with_psw() {
      this.use_psw = true
      this.style_psw = 'border-bottom: 2px solid #2d8da3;';
      this.style_msg = '';
    },
    log_with_msg() {
      this.use_psw = false
      this.style_psw = '';
      this.style_msg = 'border-bottom: 2px solid #2d8da3;';
    },
    get_captcha() {
      if (!this.username || !this.password || this.username.length < 3 || this.username.length > 16 || this.password.length < 6 || this.password.length > 16) {
        this.$message.error({
          title: '登录失败',
          type: 'error',
          message: '   账号或密码格式有误',
          duration: 1000,
        });
        return false
      }
      // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
      this.$axios({
        url: this.$settings.HOST + "user/captcha/", // 加随机数防止缓存
        method: "get",
        params: {
          username: this.username,
        },
      }).then(res => {
        let data = JSON.parse(res.data);
        // 使用initGeetest接口
        // 参数1：配置参数
        // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
        initGeetest({
          gt: data.gt,
          challenge: data.challenge,
          product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
          offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
          new_captcha: data.new_captcha
        }, this.handlerPopup);
      }).catch(error => {
        this.$message.error({
          title: '登录失败',
          type: 'error',
          message: '   账号不存在',
          duration: 1000,
        });
        // console.log(error);
        // this.$message.error(error.message)
      });
    },
    handlerPopup(captchaObj) {
      // 回调函数中  this的指向会被改变
      let self = this;
      // 在验证码被用户成功滑动后开始执行
      captchaObj.onSuccess(function () {
        let validate = captchaObj.getValidate();
        self.$axios({
          url: self.$settings.HOST + "user/captcha/",
          method: "post",
          data: {
            geetest_challenge: validate.geetest_challenge,
            geetest_validate: validate.geetest_validate,
            geetest_seccode: validate.geetest_seccode
          },
        }).then(res => {

          // r如果滑块验证码验证合格则完成登录
          self.user_login();
        }).catch(error => {
          this.$message.error(error.respond.data)
        });
      });

      // // 将验证码加到id为captcha的元素里
      let cap = document.getElementById("show_captcha");
      cap.innerHTML = '';
      captchaObj.appendTo("#show_captcha");
    },
    user_login() {
      // 判断输入框的值是否合法

      this.$axios({
        url: this.$settings.HOST + "user/login/",
        method: "post",
        data: {
          username: this.username,
          password: this.password,
        }
      }).then(res => {
        // 登陆时来判断用户是否需要记住密码 remember_me的值为True代表需要记住密码，
        if (this.remember_me) {
          // 代表用户要记住密码
          localStorage.token = res.data.token;
          localStorage.user = res.data.user;
          localStorage.user_id = res.data.user_id;
          localStorage.user_head = res.data.user_head;
        }

        if (res.data) {
          // 将token信息保存
          sessionStorage.token = res.data.token;
          sessionStorage.user = res.data.user;
          sessionStorage.user_id = res.data.user_id;
          sessionStorage.user_head = res.data.user_head;
          this.$message({
            message: "恭喜你，登陆成功",
            type: "success",
            duration: 1000,
          })
        }
        // 登陆成功后返回到首页
        this.$router.push("/")

      }).catch(error => {
        this.$message.error({
          title: '登录失败',
          type: 'error',
          message: '   账号或密码错误',
          duration: 1000,
        });
        let self = document.getElementById("show_captcha");
        self.innerHTML = '';

      })
    },
  },

}
</script>

<style scoped>
.box {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.box img {
  width: 100%;
  min-height: 100%;
}

.box .login {
  position: absolute;
  width: 500px;
  height: 400px;
  /*top: 0;*/
  left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -338px;
}

.login .login-title {
  width: 100%;
  text-align: center;
}

.login-title img {
  width: 190px;
  height: auto;
}

.login-title p {
  /*font-family: PingFangSC-Regular;*/
  font-size: 18px;
  color: #319099;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.login_box {
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.login_box .title {
  font-size: 20px;
  color: #9b9b9b;
  letter-spacing: .32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 50px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}

.login_box .title span:nth-of-type(1) {
  color: #4a4a4a;
  /*border-bottom: 2px solid #84cc39;*/
}

.inp {
  width: 350px;
  margin: 0 auto;
}

.inp input {
  outline: 0;
  width: 100%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 30px;
  font-size: 14px;
  background: #fff !important;
  text-align: left;
}

.inp input.user {
  margin-bottom: 16px;
}

.inp .rember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-top: 10px;
}

.inp .rember p:first-of-type {
  font-size: 12px;
  color: #4a4a4a;
  letter-spacing: .19px;
  margin-left: 22px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
  cursor: pointer;
}

.inp .rember input {
  outline: 0;
  width: 20px;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

.inp .rember p span {
  display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
  /*left: 20px;*/

}

#geetest {
  margin-top: 20px;
}

.login_btn {
  width: 100%;
  height: 45px;
  background: #2d8da3;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  letter-spacing: .26px;
  margin-top: 30px;
}

.inp .go_login {
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .26px;
  padding-top: 20px;
}

.inp .go_login span {
  color: #2d8da3;
  cursor: pointer;
}

.el-notification__content p {
  margin: 10px;
}

.sms-box {
  position: relative;
}

.sms-btn {
  font-size: 14px;
  color: #3e7e89;
  letter-spacing: .26px;
  position: absolute;
  right: 16px;
  top: 15px;
  cursor: pointer;
  overflow: hidden;
  background: #fff;
  border-left: 1px solid #484848;
  padding-left: 16px;
  padding-bottom: 4px;
}
</style>
