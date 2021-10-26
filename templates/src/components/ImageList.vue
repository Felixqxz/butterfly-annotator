<template>
  <b-container>
    <h2 class="page-title">Bank: {{ bankName }}</h2>
    <b-row>
      <b-col>
        <p>
          <router-link to="/">Return to the list of banks</router-link>
        </p>
      </b-col>
    </b-row>
    <form>
      <b-row>
        <b-col cols="10">
          <b-input-group>
            <b-input-group-prepend>
              <b-input-group-text>
                <ion-icon name="search-outline"></ion-icon>
              </b-input-group-text>
            </b-input-group-prepend>
            <input type="text" class="form-control" placeholder="Search..."/>
          </b-input-group>
        </b-col>
        <b-col cols="10">
          <!-- sort by: + options (dropdown menu?) TODO -->
        </b-col>
      </b-row>
    </form>
    <b-row>
      <b-col md="4" sm="6" xs="12" v-for="(image, index) in images" v-bind:key="image.id">
        <router-link :to="'/annotate/' + image.id">
          <!-- Do not use b-card: it creates automatically a b-card-body tag -->
          <div class="card card-hover no-drag image-to-annotate">
            <div class="image-hover-container">
              <img :src=image.url class="card-img-top image-hover"
                   :style="'animation-delay:' + Math.floor(index / 3) * 100 + 'ms'"
                   :alt=image.id />
            </div>
            <b-card-body class="row justify-content-between align-items-center">
              <b-col lg="9" sm="12" xs="9">
                <b-card-text>{{ image.fullDescription }}</b-card-text>
              </b-col>
              <b-col lg="3" sm="12" xs="3">TODO<!-- TODO --></b-col>
            </b-card-body>
          </div>
        </router-link>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import {mapActions} from 'vuex'

export default {
  name: 'ImageList',
  data() {
    return {
      images: [],
      bankName: '(loading)',
    }
  },
  methods: {
    ...mapActions({listImages: 'listImages'}),
    fetchImageList() {
      this.listImages(this.$route.params.bankId)
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
