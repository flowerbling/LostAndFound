<template>
  <div class="header-box">

    <div class="header">
      <div class="content">
        <div class="logo full-left">
          <router-link to="/"><img src="/static/image/logo.png" alt=""></router-link>
        </div>
        <ul class="nav full-left">
          <li v-for="(nav,index) in nav_list" :key="index"><span><a :href="'/' +nav.nav_url">{{ nav.name }}</a> </span>
          </li>
        </ul>
        <div class="login-bar full-right" v-if="token">

          <div class="login-box full-left">

            <el-avatar class="img-head" :src="this.$settings.HOST + 'media/'+ user_head"></el-avatar>
            <span class="user">{{ user }}</span>
            |
            <router-link to="/userinfo">个人中心</router-link>
            &nbsp;|&nbsp;
            <span @click="logout">退出登录</span>
          </div>
        </div>
        <!--         用户未登录信息       -->
        <div class="login-bar full-right" v-else>

          <div class="login-box full-left">
            <router-link to="/login">登录</router-link>
            &nbsp;|&nbsp;
            <router-link to="/register/">注册</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {get_content} from "../assets/common";

export default {
  name: "Header",
  data() {
    return {
      nav_list: [],
      token: '',
      user: '',
      activeIndex: '1',
      activeIndex2: '1',
      user_head: "",
    };
  },
  methods: {
    get_all_nav() {
      this.$axios.get(this.$settings.HOST + "index/nav/").then(response => {
        this.nav_list = response.data
      })
    },

    get_user() {
      if (localStorage.token) {
        sessionStorage.token = localStorage.token
      }
      if (localStorage.user) {
        sessionStorage.user = localStorage.user
      }
      if (localStorage.user_head) {
        sessionStorage.user_head = localStorage.user_head
      }
      if (localStorage.user_id) {
        sessionStorage.user_id = localStorage.user_id
      }
      if (localStorage.username) {
        sessionStorage.username = localStorage.username
      }
      this.token = sessionStorage.token || localStorage.token;

    },
    logout() {
      localStorage.clear()
      sessionStorage.clear()
      window.location.href = ''
    }

  },
  created() {
    this.get_all_nav();
    this.get_user();
    this.user = get_content(sessionStorage.user, 0, 6) || get_content(localStorage.user, 0, 6)
    this.user_head = sessionStorage.user_head || localStorage.user_head
    if (!this.user) {
      this.user = get_content(sessionStorage.user || localStorage.user, 0, 6)
    }
    if (!this.user_head) {
      this.user_head = sessionStorage.user_head || localStorage.user_head
    }
  }

}
</script>

<style scoped>

.header-box {
  height: 80px;
}

.user {
  font-weight: bold;
}

.header {
  width: 100%;
  height: 80px;
  box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  margin: auto;
  z-index: 99;
  background: #fff;
}

.header .content {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.header .content .logo {
  height: 80px;
  line-height: 80px;
  margin-right: 50px;
  cursor: pointer; /* 设置光标的形状为爪子 */
}

.header .content .logo img {
  vertical-align: middle;
  height: 80px;
  line-height: 80px;
  margin-right: 50px;
}

.header .nav li {
  float: left;
  height: 80px;
  line-height: 80px;
  margin-right: 30px;
  font-size: 16px;
  color: #4a4a4a;
  cursor: pointer;
}

.header .nav li span {
  padding-bottom: 16px;
  padding-left: 5px;
  padding-right: 5px;
}

.header .nav li span a {
  display: inline-block;
  font-size: 18px;
}

.header .nav li .this {
  color: #4a4a4a;
  border-bottom: 4px solid #ffc210;
}

.header .nav li:hover span {
  color: #000;
}

.header .login-bar {
  height: 80px;
}

.header .login-bar .login-box {
  margin-top: 33px;
}

.header .login-bar .login-box span {
  color: #4a4a4a;
  cursor: pointer;
}

.header .login-bar .login-box span:hover {
  color: #000000;
}

a {
  text-decoration: none;
  color: #333;
}

.member {
  display: inline-block;
  height: 34px;
  margin-left: 20px;
}

.member img {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-block;
}

.member img:hover {
  border: 1px solid yellow;
}

.header .login-bar .login-box1 {
  margin-top: 16px;
}

a:hover {
  display: inline-block;
}

.img-head {
  vertical-align: middle;
}
</style>
