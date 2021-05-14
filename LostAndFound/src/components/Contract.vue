<template>
  <div>
    <Header></Header>
    <div class=" let-vertical" style="margin-left: 650px">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>联系我们</span>
        </div>
        <div class="text item">
          联系电话:13643584702
        </div>
        <div class="text item">
          联系QQ:1254161251
        </div>
      </el-card>

    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header";
import Footer from "./Footer";

export default {
  name: "Contract",
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both
}

.box-card {
  width: 480px;
}
</style>
