<template>
  <div class="box">
    <img src="/static/image/bg.png" alt="">

    <div class="register">
      <div class="register_logo">
        <a href="/"><img src="/static/image/logo.png" alt="花朵闪闪-花卉中心"></a>
        <p>丢了东西不要怕，寻物局帮你找到它！</p>
      </div>
      <div class="register_box">
        <div class="register-title">高校失物招领系统注册</div>
        <div class="inp">
          <input v-model="phone" type="text" placeholder="手机号码" class="user" @blur="check_phone">
          <input v-model="username" type="text" placeholder="用户名" class="user_name" @blur="check_username">
          <br><br>
          <input v-model="password" type="password" placeholder="登录密码" class="user">
          <div id="geetest"></div>
          <div class="sms-box">
            <input v-model="code" type="text" maxlength="6" placeholder="输入验证码" class="user">
            <div class="sms-btn" @click="get_code" v-if="show">发送验证码</div>
            <div class="sms-btn"  v-else>已发送 {{ left_time }}</div>
          </div>
          <button class="register_btn" @click="user_register">注册</button>
          <p class="go_login">已有账号
            <router-link to="/login">直接登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      phone: "",
      password: "",
      username: '',
      code: "",
      phone_true: false,
      password_true: false,
      username_ture: false,
      text: "获取验证码",
      left_time: '',
      show:true,
      the_set:'',
    }
  },
  methods: {
    // 用户注册的逻辑
    user_register() {
      if (this.username.length < 3 || this.username > 16) {
        this.username_ture = false
        this.$message.error("用户名格式有误(3-16位)")
        return false;
      }
      if (this.password.length < 3 || this.password.length > 16) {
        this.password_true = false;
        this.$message.error("密码格式有误")
        return false
      }
      if (!/^1[3-9]\d{9}$/.test(this.phone)) {
        this.phone_true = false;
        this.$message.error("手机号格式有误")
        return false
      }
      if (this.code.length !== 6) {
        this.password_true = false;
        this.$message.error("验证码格式有误")
        return false
      }

      this.$axios({
        url: this.$settings.HOST + "user/register/",
        method: "post",
        data: {
          phone: this.phone,
          password: this.password,
          username: this.username,
          code: this.code,

        }
      }).then(res => {
        if (res.data.token) {
          // 保存用户登陆状态

          this.$message.success("注册成功，即将跳转到首页")
          // 跳转到首页
          this.$router.push("/");
        }
      }).catch(error => {
        this.$message.error("用户名或密码不合格")
      })
    },
    // 检查手机号是否被注册
    check_phone() {
      this.$axios({
        url: this.$settings.HOST + "user/phone/",
        method: "get",
        params: {
          phone: this.phone,
        }
      }).then(res => {
        this.phone_true = true
      }).catch(error => {
        this.phone_true = false;
        this.$message.error(error.response.data)
      })
    },
    check_username() {
      this.$axios({
        url: this.$settings.HOST + "user/username/",
        method: "get",
        params: {
          username: this.username,
        }
      }).then(res => {
        this.username_ture = true
      }).catch(error => {
        this.username_ture = false
        this.$message.error(error.response.data)
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
      if (!/^1[3-9]\d{9}$/.test(this.phone)) {
        this.phone_true = false;
        this.$message.error("手机号格式有误")
        return false
      }
      if (!this.phone_true) {
        this.$message.error("请检查你的手机号")
        return false;
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
        console.log(error);
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

.register_logo {
  margin-top: -100px;
  text-align: center;
  /*margin: 0 auto;*/
}

.register_logo img {
  width: 190px;
  height: auto;
}


.register_logo p {
  font-size: 18px;
  color: #319099;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.box .register {
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

.register .register-title {
  width: 100%;
  font-size: 24px;
  text-align: center;
  padding-top: 30px;
  padding-bottom: 30px;
  color: #4a4a4a;
  letter-spacing: .39px;
}

.register-title img {
  width: 190px;
  height: auto;
}

.register-title p {
  /*font-family: PingFangSC-Regular;*/
  font-size: 18px;
  color: #fff;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.register_box {
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.register_box .title {
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

.register_box .title span:nth-of-type(1) {
  color: #4a4a4a;
  border-bottom: 2px solid #2d8da3;
}

.inp {
  width: 350px;
  margin: 0 auto;
}

.inp input {
  /*border: 0;*/
  outline: 0;
  width: 100%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
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
  width: 30px;
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

.register_btn {
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

.sms-box {
  position: relative;
}

.sms-btn {
  font-size: 14px;
  color: #2d8da3;
  letter-spacing: .26px;
  position: absolute;
  right: 16px;
  top: 10px;
  cursor: pointer;
  overflow: hidden;
  background: #fff;
  border-left: 1px solid #484848;
  padding-left: 16px;
  padding-bottom: 4px;
}
</style>
