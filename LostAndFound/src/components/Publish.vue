<template>
  <div>
    <Header></Header>
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px"
             class="demo-ruleForm let-middle let-vertical">
      <el-form-item label="发布类型" prop="is_lost">
        <el-select v-model="ruleForm.is_lost" placeholder="请选择发布类型">
          <el-option label="发布失物" value="1"></el-option>
          <el-option label="发布拾物" value="0"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="物品名称" prop="name">
        <el-input v-model="ruleForm.name"></el-input>
      </el-form-item>
      <el-form-item label="物品类型" prop="region">
        <el-select v-model="ruleForm.the_type" placeholder="请选择物品类型">
          <el-option label="文件" value="0"></el-option>
          <el-option label="文具" value="1"></el-option>
          <el-option label="日常用品" value="2"></el-option>
          <el-option label="玩具" value="3"></el-option>
          <el-option label="电子产品" value="4"></el-option>
          <el-option label="衣服" value="5"></el-option>
          <el-option label="其他" value="6"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="地点(丢失/拾取)" prop="name">
        <el-input v-model="ruleForm.area"></el-input>
      </el-form-item>
      <el-form-item label="时间(丢失/拾取)" required>
        <el-col :span="11">
          <el-form-item prop="date1">
            <el-date-picker
              v-model="ruleForm.date1"
              type="datetime"
              placeholder="选择日期时间">
            </el-date-picker>
          </el-form-item>
        </el-col>
      </el-form-item>
      <el-form-item label="物品描述" prop="description">
        <el-input type="textarea" v-model="ruleForm.description"></el-input>
      </el-form-item>
      <el-form-item label="物品图片" prop="goods_image">
        <el-upload
          class="upload-demo"
          :action="this.$settings.HOST + 'goods/upload/'"
          :on-success="handleAvatarSuccess"
          :file-list="fileList"
          list-type="picture">
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">立即发布</el-button>
      </el-form-item>

    </el-form>
    <Footer></Footer>
  </div>

</template>

<script>
import Header from "./Header";
import Footer from "./Footer";
import {check_user_login} from "../assets/common";

export default {
  name: "Publish",
  data() {
    return {
      user_id: '',
      fileList: [],
      files: [],
      ruleForm: {
        is_lost: '',
        name: '',
        the_type: '',
        date1: '',
        description: '',
        area: ''
      },
      rules: {
        name: [
          {required: true, message: '请输入物品名称', trigger: 'blur'},
          {min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur'}
        ],
        is_lost: [
          {required: true, message: '请选择发布类型', trigger: 'change'}
        ],
        the_type: [
          {required: true, message: '请选择物品类型', trigger: 'change'}
        ],
        date1: [
          {type: 'date', required: true, message: '请选择日期', trigger: 'change'}
        ],
        date2: [
          {type: 'date', required: true, message: '请选择时间', trigger: 'change'}
        ],
        area: [
          {required: true, message: '请填写地点', trigger: 'blur'}
        ],
        desc: [
          {required: true, message: '请填写物品描述', trigger: 'blur'}
        ]
      }


    }
  },

  components: {
    Header,
    Footer,
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let token = check_user_login();
          if (!token) {
            this.$message.error("登录失效,请重新登录")
            return false
          }
          this.$axios.post(this.$settings.HOST + "goods/lost_info/", {
            'name': this.ruleForm.name,
            'is_lost': this.ruleForm.is_lost,
            'the_type': this.ruleForm.the_type,
            'area': this.ruleForm.area,
            'date': this.ruleForm.date1,
            'description': this.ruleForm.description,
            'user': sessionStorage.user_id || localStorage.user_id,
          }, {headers: {"Authorization": "jwt " + token}}).then(res => {
            console.log(res.data)
            for (let i = 0; i < this.files.length; i++) {
              this.$axios.post(this.$settings.HOST + 'goods/images/', {
                  "goods": res.data.id,
                  'image_url': this.files[i].image_url
                }
                , {
                  headers: {
                    "Authorization": "jwt " + token
                  }
                }).then(res => {
                this.$message.success("发布成功!")
                location.href = ''
              })

            }

          })

        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    handleAvatarSuccess(res, file, fileList) {
      console.log(file)
      this.files.push({'image_url': res.data})
    },
    check_user_info() {
      let token = localStorage.token || sessionStorage.token;
      if (!token) {
        let self = this
        this.$alert("未登录或登录失效,请先登录", {
          callback() {
            self.$router.push('/login')
          }
        })
      }
      this.$axios.get(this.$settings.HOST + "user/userinfo/?id=" + sessionStorage.user_id, {headers: {"Authorization": "jwt " + token}}).then(res => {
        let userinfo = res.data.data
        let self = this
        console.log(res.data)
        if (/.{2,255}/.test(userinfo.cls) && /.{2,255}/.test(userinfo.object) && /.{2,255}/.test(userinfo.qq) && /.{2,255}/.test(userinfo.con_phone) && /.{2,255}/.test(userinfo.name) && /.{2,255}/.test(userinfo.qq)) {
        } else {
          this.$alert("请先完善个人信息", {
            callback() {
              self.$router.push("/userinfo/")
              return false
            }
          })
        }

      })
    }
  },
  created() {
    this.check_user_info()
  },


}

</script>

<style scoped>

</style>
