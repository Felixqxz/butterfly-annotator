<template>
  <div class="container">
    <h2 class="page-title">Bank: {{ bankName }}</h2>
    <form>
      <div class="row">
        <div class="col-10">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"><ion-icon name="search-outline"></ion-icon></span>
            </div>
            <input type="text" class="form-control" placeholder="Search..."/>
          </div>
        </div>
        <div class="col-2">
          <!-- sort by: + options (dropdown menu?) TODO -->
        </div>
      </div>
    </form>
    <div class="row">
      <div class="col-md-4 col-sm-6 col-xs-12" v-for="(image, index) in images" v-bind:key="image.id">
        <div class="card card-hover no-drag image-to-annotate">
          <div class="image-hover-container">
            <img :src=image.url class="card-img-top image-hover"
                 :style="'animation-delay:' + Math.floor(index / 3) * 100 + 'ms'"
                 :alt=image.id />
          </div>
          <div class="card-body row justify-content-between align-items-center">
            <div class="col-lg-9 col-sm-12 col-xs-9"><span class="card-text">{{ image.fullDescription }}</span></div>
            <div class="col-lg-3 col-sm-12 col-xs-3">TODO<!-- TODO --></div>
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
