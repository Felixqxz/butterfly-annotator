<template>
  <div id="app">
    <Header/>
    <router-view class="container container-fluid"/>
    <Footer/>
  </div>
</template>

<style>
.no-drag { /* TODO: move this in a .css file */
  user-drag: none;
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}

#app {
  position: relative;
  min-height: 95vh;
}
</style>
<script>
import Header from './components/Header'
import Footer from './components/Footer'

export default {
  components: {
    'Header': Header,
    'Footer': Footer,
  },
}
</script>