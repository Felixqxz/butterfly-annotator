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
  data() {
    return {
      msg: '',
    }
  },
  methods: {
    getMessage() {
      axios.get(this.$hostname)
        .then((res) => {
          this.msg = res.data
        })
        .catch((error) => {
          console.error(error) // TODO: handle error correctly
        })
    },
  },
  created() {
    this.getMessage()
  },
  components: {
    Header
  }
}
</script>