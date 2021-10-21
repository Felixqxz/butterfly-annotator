<template>
  <div>
    <div class="jumbotron">
      <h1>Test!</h1>
      <h2>This is bank {{ bankName }}</h2>
    </div>
    <div class="container container-fluid">
      <figure class="figure col col-md-4 col-sm-6 col-xs-12 no-drag" v-for="image in images" v-bind:key="image.id">
        <img :src=image.url class="figure-img img-fluid rounded" :alt=image.id />
        <figcaption class="figure-caption text-center">{{ image.fullDescription }}</figcaption>
      </figure>
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

    //display all the images the user uploaded
    getAllImages() {
      axios
        .get(this.$hostname + "/api/image/getImage")
        .then((res) => {
          let data = res.data;
          this.Images = data.images;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.fetchImageList()
    //this.getAllImages()
  },
}
</script>
