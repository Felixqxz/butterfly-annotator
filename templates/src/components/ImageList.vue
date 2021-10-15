<template>
  <div class="jumbotron">
    <h1>Test!</h1>
    {{ $route.params.bankId }}
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ImageList',
  data() {
    return {
      images: [],
    }
  },
  methods: {
    fetchImageList() {
      axios.get(this.$hostname + '/api/dir/bank/' + this.$route.params.bankId)
        .then(res => {
          this.images = res
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  created() {
    this.fetchImageList()
  },
}
</script>
