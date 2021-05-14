import Vue from 'vue'
import Router from 'vue-router'
import Index from "../components/Index";
import Login from "../components/Login";
import Register from "../components/Register";
import Userinfo from "../components/Userinfo";
import Publish from "../components/Publish";
import LostGoods from "../components/LostGoods";
import PickGoods from "../components/PickGoods";
import Published from "../components/Published";
import Contract from "../components/Contract";


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {path: '/index', name: 'Index', meta: {'title': '失物招领'}, component: Index},
    {path: '/login', name: 'Login', meta: {'title': '登录-失物招领'}, component: Login},
    {path: '/register', name: 'Register', meta: {'title': '注册-失物招领'}, component: Register},
    {path: '/userinfo', name: 'Userinfo', meta: {'title': '个人信息'}, component: Userinfo},
    {path: '/publish', name: 'Publish', meta: {'title': '发布物品'}, component: Publish},
    {path: '/lost_info', name: 'LostGoods', meta: {'title': '查看失物'}, component: LostGoods},
    {path: '/pick_info', name: 'PickGoods', meta: {'title': '查看失物'}, component: PickGoods},
    {path: '/published', name: 'Published', meta: {'title': '已发布物品'}, component: Published},
    {path: '/contract', name: 'Contract', meta: {'title': '联系我们'}, component: Contract},
    {path: '/', name: 'Index', redirect: '/index'}

  ],
  linkActiveClass: 'active'
})
