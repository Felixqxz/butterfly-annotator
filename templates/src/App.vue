<template>
  <div id="app">
    <Header/>
    <router-view class="container container-fluid"/>
    <Footer/>
  </div>
</template>

<style>
#app {
  position: relative;
  min-height: 95vh;
}

@import url('https://fonts.googleapis.com/css2?family=Nunito:ital@0;1&display=swap');

* {
  font-family: 'Nunito', sans-serif !important;
}

a {
  text-decoration: none !important;
}

.no-drag {
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}

.page-title {
  margin-top: 1rem;
}

.card-hover {
  transition: border-color 0.3s;
}

.card-hover:hover {
  border-color: gray;
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
