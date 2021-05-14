<template>
  <div id="app">
  <router-view></router-view>

  </div>
</template>

<script>
import Header from "./components/Header";
import Footer from "./components/Footer";

export default {
  name: 'App',
  components: {
    Header: Header,
    Footer: Footer,
  }
}
</script>

<style>

</style>
