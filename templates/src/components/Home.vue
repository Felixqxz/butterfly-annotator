<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
import axios from 'axios'

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
}
</script>