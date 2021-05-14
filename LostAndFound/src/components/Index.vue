<template>
  <el-container>
    <el-header><Header></Header></el-header>
    <el-main class="let-middle">
      <img src="static/image/laf.webp" alt="">
    </el-main>
    <el-footer><Footer></Footer></el-footer>
  </el-container>

</template>

<script>
import Header from "./Header";
import Footer from "./Footer";

export default {
  name: "Index",
  components: {
    Header: Header,
    Footer: Footer
  }
}
</script>

<style scoped>

</style>
