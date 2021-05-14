<template>
  <div>
    <Header></Header>
    <div class="let-middle let-vertical">
      <div>
        <el-row class="let-far">
          <el-button :type="this.the_type==='all'?'primary':'default'" @click="the_type='all'">全部</el-button>
          <el-button :type="this.the_type==='0'?'primary':'default'" @click="the_type='0'">文件</el-button>
          <el-button :type="this.the_type==='1'?'primary':'default'" @click="the_type='1'">文具</el-button>
          <el-button :type="this.the_type==='2'?'primary':'default'" @click="the_type='2'">日常用品</el-button>
          <el-button :type="this.the_type==='3'?'primary':'default'" @click="the_type='3'">玩具</el-button>
          <el-button :type="this.the_type==='4'?'primary':'default'" @click="the_type='4'">电子产品</el-button>
          <el-button :type="this.the_type==='5'?'primary':'default'" @click="the_type='5'">衣服</el-button>
          <el-button :type="this.the_type==='6'?'primary':'default'" @click="the_type='6'">其他</el-button>
        </el-row>

        <el-card class="box-card let-far" v-for="(the_lost,index) in the_list" :key="index">
          <div slot="header" class="clearfix">
            <div class="full-left">
              <el-avatar :src="$settings.HOST + 'media/' + the_lost.user.user_head" class="img-head"></el-avatar>
              <span class="name">{{ the_lost.user.name }}</span>
              <span> # {{ the_lost.name }}</span>
              <el-tag>{{ the_types[the_lost.the_type] }}</el-tag>
            </div>
          </div>
          <!--          <div v-for="o in 4" :key="o" class="text item">-->
          <!--            {{ '列表内容 ' + o }}-->
          <!--          </div>-->
          <div>
            <div class="the_list">
              <el-tag type="info" class="list_title">物品描述</el-tag>
              <span class="list_Content">--{{ the_lost.description }}</span>
            </div>
            <div class="the_list">
              <el-tag type="info" class="list_title">地点</el-tag>
              <span class="list_Content">--{{ the_lost.area }}</span>
            </div>
            <div class="the_list">
              <el-tag type="info" class="list_title">时间</el-tag>
              <span class="list_Content">--{{ the_lost.date }}</span>
            </div>
            <div class="the_list">
              <el-tag type="info" class="list_title">物品描述</el-tag>
              <span class="list_Content">--{{ the_lost.description }}</span>
            </div>
            <div class="the_list">
              <el-tag type="info" class="list_title">联系电话</el-tag>
              <span class="list_Content">--{{ the_lost.user.con_phone }}</span>
            </div>
            <div class="the_list">
              <el-tag type="info" class="list_title">联系QQ</el-tag>
              <span class="list_Content">--{{ the_lost.user.qq }}</span>
            </div>
            <div class="the_list">
              <el-tag type="info" class="list_title">物品图片</el-tag>
              <el-image
                class="img-head let-far-left"
                v-for="(image_url,index) in the_lost.images"
                :key="index"
                style="width: 100px; height: 100px"
                :src="$settings.HOST + 'media/' + image_url.image_url">
              </el-image>
            </div>
            <div class="the_list">
              <el-tag type="info" class="list_title">物品状态</el-tag>
              <el-switch
                v-model="the_lost.status"
                active-text="有效"
                inactive-text="失效"
                :change="switch_change(the_lost.id,the_lost.status)">
              </el-switch>
            </div>
          </div>
        </el-card>
        <el-pagination
          class="let-far"
          background
          :page-size="filters.size"
          layout="prev, pager, next, sizes"
          :page-sizes="[2, 3, 5, 10]"
          @size-change="size_change"
          @current-change="change_page"
          :total="total">
        </el-pagination>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header";
import Footer from "./Footer";
import {check_user_login} from "../assets/common";

export default {
  name: "Published",
  components: {
    Header,
    Footer
  },
  methods: {
    switch_change(goods, status) {
      let token = check_user_login();
      if (!token) {
        this.$message.error("登录失效,请重新登录")
        return false
      }
      this.$axios.patch(this.$settings.HOST + 'user/goods_status/', {
          'id': goods,
          'status': status
        }
        ,
        {
          headers: {
            "Authorization":
              "jwt " + token
          }
        }
      )
    },
    size_change(size) {
      this.filters.size = size;
      // 改变每次分页展示的数量后，都展示更新后的第一页
      this.filters.page = 1;
      this.getAllGoods();
    }
    ,
    change_page(page) {
      this.filters.page = page;
      this.getAllGoods();
    }
    ,
    getAllGoods() {
      let filters = {
        // 将每次切换后的页面传递过去
        page: this.filters.page,
        size: this.filters.size,
      }

      if (this.the_type === 'all') {
        this.$axios.get(this.$settings.HOST + 'user/goods_info/', {params: filters}).then(
          res => {
            console.log(res.data)
            this.the_list = res.data.results
            this.total = res.data.count
          }
        )
      } else {
        this.$axios.get(this.$settings.HOST + 'user/goods_info/?the_type=' + this.the_type, {params: filters}).then(
          res => {
            this.the_list = res.data.results
            this.total = res.data.count

          }
        )
      }
    }
    ,
  },
  data() {
    return {
      message: [],
      the_type: "all",
      the_types: ['文件', '文具', '日常用品', '玩具', '电子产品', '衣服', '其他'],
      the_list: [],
      total: 0,
      filters: {
        size: 2,
        page: 1,
      }
    }

  }
  ,
  watch: {
    the_type() {
      this.getAllGoods()
    }
    ,

  }
  ,
  created() {
    let token = localStorage.token || sessionStorage.token;
    if (!token) {
      let self = this
      this.$alert("未登录或登录失效,请先登录", {
        callback() {
          self.$router.push('/login')
        }
      })
    }
    this.getAllGoods()
  }
}

</script>

<style scoped>

</style>
