<template>
  <div>
    <Header></Header>
    <div class="let-middle let-vertical">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="用户头像" prop="user-head">
          <el-upload
            class="avatar-uploader"
            :action='this.$settings.HOST + "user/upload/"'
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="this.$settings.HOST + 'media/' + imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item label="真实姓名" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="所在专业" prop="object">
          <el-input v-model="ruleForm.object"></el-input>
        </el-form-item>
        <el-form-item label="所在班级" prop="class">
          <el-input v-model="ruleForm.cls"></el-input>
        </el-form-item>
        <el-form-item label="QQ号" prop="qq">
          <el-input v-model="ruleForm.qq"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="con_phone">
          <el-input v-model="ruleForm.con_phone"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="ruleForm.gender">
            <el-radio :label=true>男</el-radio>
            <el-radio :label=false>女</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>

          <el-button type="primary" @click="dialogFormVisible = true">修改密码</el-button>

          <el-dialog title="收货地址" :visible.sync="dialogFormVisible" :close-on-click-modal="false"
                     :close-on-press-escape="false" :show-close="false">
            <el-form :model="form">
              <el-form-item label="旧密码" :label-width="formLabelWidth">
                <el-input v-model="form.old_password" autocomplete="off" type="password"></el-input>
              </el-form-item>
              <el-form-item label="新密码" :label-width="formLabelWidth" class="let-far">
                <el-input v-model="form.new_password" autocomplete="off" type="password"></el-input>
              </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="cancel_change_password">取 消</el-button>
              <el-button type="primary" @click="change_password">确 定</el-button>
            </div>
          </el-dialog>

        </el-form-item>
      </el-form>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header";
import Footer from "./Footer";
import {checkPhone} from "../assets/rules";
import {check_user_login, force_login} from "../assets/common";

export default {
  name: "Userinfo",
  data() {
    return {
      dialogFormVisible: false,
      form: {
        old_password: '',
        new_password: '',
      },
      formLabelWidth: '120px',
      user_id: '',
      imageUrl: '',
      ruleForm: {
        name: '',
        object: '',
        cls: '',
        gender: '',
        qq: '',
        con_phone: '',
      },
      rules: {
        name: [
          {required: true, message: '请输入真实姓名', trigger: 'blur'},
          {min: 2, max: 8, message: '长度在 2 到 8 个字符', trigger: 'blur'}
        ],
        object: [
          {required: true, message: '请输入专业', trigger: 'blur'},
          {min: 2, max: 8, message: '长度在 2 到 8 个字符', trigger: 'blur'}
        ],
        cls: [
          {required: true, message: '请输入班级', trigger: 'blur'},
          {min: 2, max: 8, message: '长度在 2 到 8 个字符', trigger: 'blur'}
        ],
        qq: [
          {required: true, message: '请输入QQ', trigger: 'blur'},
          {min: 6, max: 10, message: '长度在 6-10 个字符', trigger: 'blur'}
        ],
        con_phone: [
          {required: true, message: '请输入手机号', trigger: 'blur'},
          {min: 11, max: 11, message: '长度为 11 个字符', trigger: 'blur'},
          {validator: checkPhone, trigger: 'blur'}
        ],
      }
    };
  },
  methods: {
    cancel_change_password() {
      this.form.new_password = ''
      this.form.old_password = ''
      this.dialogFormVisible = false
    },
    change_password() {
      if (this.form.new_password.length < 3 || this.form.new_password.length > 16) {
        this.$message.error("新密码必须在3-16位")
        return false
      }
      if (this.form.old_password.length < 3 || this.form.old_password.length > 16) {
        this.$message.error("旧密码必须在3-16位")
        return false
      }
      let token = check_user_login();
      if (!token) {
        return false
      }
      this.$axios.patch(this.$settings.HOST + 'user/change_pass/', {
        'id': sessionStorage.user_id || localStorage.user_id,
        'old_password': this.form.old_password,
        'new_password': this.form.new_password,
      }, {
        headers: {
          "Authorization": "jwt " + token
        }
      }).then(res => {
          console.log(res)
          this.dialogFormVisible = false
          this.$message.success("密码修改成功,请重新登录")
          sessionStorage.clear()
          localStorage.clear()
          location.href = '/login'
        }
      ).catch(error => {
        this.$message.error(error.response.data.message)
      })
    },
    handleAvatarSuccess(res, file) {
      this.imageUrl = res.data
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG/PNG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    },
    submitForm(formName) {
      let token = check_user_login();
      if (!token) {
        return false
      }
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.put(
            this.$settings.HOST + "user/userinfo/", {
              'id': this.user_id,
              "cls": this.ruleForm.cls,
              "object": this.ruleForm.object,
              "name": this.ruleForm.name,
              "user_head": this.imageUrl,
              "gender": this.ruleForm.gender,
              "qq": this.ruleForm.qq,
              "con_phone": this.ruleForm.con_phone,
            },
            {
              headers: {
                "Authorization": "jwt " + token
              }
            }
          ).then(res => {
            this.$message.success("保存成功")
            localStorage.user_head = this.imageUrl
            sessionStorage.user_head = this.imageUrl
            location.href = ""
          }).catch(error => {
            console.log(error)
            this.$message.error(error)
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    getUserInfo() {
      let token = check_user_login();
      if (!token) {
        this.$message.error("登录失效,请重新登录")
        return false
      }
      this.$axios.get(this.$settings.HOST + "user/userinfo/?id=" + this.user_id, {headers: {"Authorization": "jwt " + token}}).then(res => {
        let userinfo = res.data.data
        this.ruleForm.cls = userinfo.cls
        this.ruleForm.object = userinfo.object
        this.ruleForm.con_phone = userinfo.con_phone
        this.ruleForm.qq = userinfo.qq
        this.ruleForm.name = userinfo.name
        this.ruleForm.gender = userinfo.gender
        this.imageUrl = userinfo.user_head
      })
    },
  },

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


    this.user_id = sessionStorage.user_id || localStorage.user_id;
    this.getUserInfo()

  },
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
