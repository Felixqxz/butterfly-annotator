<template>
  <div id="app">
    <Header/>
    <Alert/>
    <router-view class="container container-fluid"/>
    <Footer/>
  </div>
</template>

<style>
#app {
  position: relative;
  min-height: 95vh;
}
</style>
<script>
import Header from './components/Header'
import Footer from './components/Footer'
import Alert from './components/Alert'

export default {
  components: {
    'Header': Header,
    'Footer': Footer,
    'Alert': Alert
  },
}
</script>
