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

        <el-card class="box-card let-far" v-for="(the_lost,index) in the_list" :key="index" v-if="the_lost.is_lost">
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
              <el-tag type="info" class="list_title">留言区</el-tag>
              <el-button class="full-right" type="primary" @click="open(the_lost.id)">点击添加留言</el-button>
              <el-table
                :data="the_lost.goods_message"
                height="160"
                border
                style="width: 100%">
                <el-table-column
                  prop="date"
                  label="日期"
                  width="180">
                </el-table-column>
                <el-table-column
                  prop="con_phone"
                  label="联系手机"
                  width="120">
                </el-table-column>
                <el-table-column
                  prop="qq"
                  label="联系QQ"
                  width="120">
                </el-table-column>

                <el-table-column
                  prop="name"
                  label="姓名"
                  width="120">
                </el-table-column>
                <el-table-column
                  prop="content"
                  label="内容"
                  width="640">
                </el-table-column>
              </el-table>
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
  name: "LostGoods",
  components: {
    Header,
    Footer
  },
  methods: {
    check_user_info() {
      let token = localStorage.token || sessionStorage.token;
      if (!token) {
        let self = this
        this.$alert("未登录或登录失效,请先登录", {
          callback() {
            self.$router.push('/login')
            return false
          }
        })
      }
      let userinfo = {}
      this.$axios.get(this.$settings.HOST + "user/userinfo/?id=" + sessionStorage.user_id, {headers: {"Authorization": "jwt " + token}}).then(res => {
        userinfo = res.data.data
        console.log(res.data.data)
        console.log(/.{2,255}/.test(userinfo.cls) && /.{2,255}/.test(userinfo.object) && /.{2,255}/.test(userinfo.qq) && /.{2,255}/.test(userinfo.con_phone) && /.{2,255}/.test(userinfo.name));


      })
      return /.{2,255}/.test(userinfo.cls) && /.{2,255}/.test(userinfo.object) && /.{2,255}/.test(userinfo.qq) && /.{2,255}/.test(userinfo.con_phone) && /.{2,255}/.test(userinfo.name);

    },
    open(goods) {
      let self = this
      console.log(this.check_user_info())
      if (this.check_user_info()) {
        this.$prompt('请输入留言内容', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /.{1,240}/,
          inputErrorMessage: '不可以为空'
        }).then(({value}) => {
          let token = check_user_login();
          if (!token) {
            this.$message.error("登录失效,请重新登录")
            return false
          }
          this.$axios.post(this.$settings.HOST + 'goods/goods_message/', {
            'user': localStorage.user_id || sessionStorage.user_id,
            'goods': goods,
            'content': value
          }, {
            headers: {
              "Authorization": "jwt " + token
            }
          }).then(
            this.$message({
              type: 'success',
              message: '添加成功',
            }),
            this.getAllGoods()
          )
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      } else {
        this.$alert("请先完善个人信息", {
          callback() {
            self.$router.push("/userinfo/")
          }
        })
      }
    },
    size_change(size) {
      this.filters.size = size;
      // 改变每次分页展示的数量后，都展示更新后的第一页
      this.filters.page = 1;
      this.getAllGoods();
    },
    change_page(page) {
      this.filters.page = page;
      this.getAllGoods();
    },
    getAllGoods() {
      let filters = {
        // 将每次切换后的页面传递过去
        page: this.filters.page,
        size: this.filters.size,
      }

      if (this.the_type === 'all') {
        this.$axios.get(this.$settings.HOST + 'goods/lost_info/', {params: filters}).then(
          res => {
            console.log(res.data)
            this.the_list = res.data.results
            this.total = res.data.count
          }
        )
      } else {
        this.$axios.get(this.$settings.HOST + 'goods/lost_info/?the_type=' + this.the_type, {params: filters}).then(
          res => {
            this.the_list = res.data.results
            this.total = res.data.count

          }
        )
      }
    }

  }
  ,
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

  },
  watch: {
    the_type() {
      this.getAllGoods()
    },

  },
  created() {
    this.getAllGoods()
  }
}
</script>

<style scoped>


</style>
