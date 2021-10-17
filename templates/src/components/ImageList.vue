<template>
  <div class="container">
    <h2 class="text-center">Bank: {{ bankName }}</h2>
    <div class="row">
      <div class="col-md-4 col-sm-6 col-xs-12" v-for="(image, index) in images" v-bind:key="image.id">
        <div class="card no-drag image-to-annotate">
          <div class="image-hover-container">
            <img :src=image.url class="card-img-top image-hover"
                 :style="'animation-delay:' + Math.floor(index / 3) * 100 + 'ms'"
                 :alt=image.id />
          </div>
          <div class="card-body">
            <span class="card-text">{{ image.fullDescription }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ImageList',
  data() {
    return {
      images: [],
      bankName: '(loading)',
    }
  },
  methods: {
    fetchImageList() {
      axios.get(this.$hostname + '/api/bank/' + this.$route.params.bankId)
          .then(res => {
            if (res.status !== 200) {
              console.log('Could not load DB => ERROR, HTTP status=' + res.status) // TODO: handle correctly
            } else {
              let data = res.data
              this.images = data.images
              this.bankName = data.bankName
            }
          })
          .catch(err => {
            console.log(err) // TODO: handle errors properly
          })
    },
  },
  created() {
    this.fetchImageList()
  },
}
</script>
