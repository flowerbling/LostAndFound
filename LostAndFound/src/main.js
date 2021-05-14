// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import "../static/css/global.css"
import "../static/js/gt"
import axios from "axios"
import store from './store'
import settings from "./settings";

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.prototype.$axios = axios



Vue.prototype.$settings = settings;
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  store
})





Vue.directive('title', {
  inserted: function (el, binding) {
    document.title = el.dataset.title
  },


})
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
})

