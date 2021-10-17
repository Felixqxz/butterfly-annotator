<template>
  <div>
    <Header></Header>
  </div>
</template>

<script>
import axios from 'axios'
import Header from '../components/Header.vue'

export default {
  name: 'Home',
  components: {
    Header
  }
}
</script>