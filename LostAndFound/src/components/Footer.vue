<template>
  <div class="footer">
    <ul>
      <li v-for="(nav,index) in foot_list" :key="index">
<a class="foot" :href="nav.nav_url">{{ nav.name }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      foot_list: []
    }
  },
  methods: {
    get_all_nav() {
      this.$axios.get(this.$settings.HOST + "index/foot/").then(response => {
        this.foot_list = response.data
      })
    }
  },
  created() {
    this.get_all_nav();
  }

}
</script>

<style scoped>
.footer {
  width: 100%;
  height: 128px;
  background: #25292e;
  color: #fff;
}

.footer ul {
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 810px;
}

.footer ul li {
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
}

.foot {
  font-size: 18px;
  color: #fff;
}

.footer ul::after {
  content: "";
  display: block;
  clear: both;
}


.footer p {
  text-align: center;
  font-size: 12px;
}
</style>
