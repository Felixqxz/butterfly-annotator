<template>
  <b-container>
    <h2 class="page-title">Bank: {{ bankName }}</h2>
    <b-row>
      <b-col sm="3">
        <p>
          <router-link to="/">Return to the list of banks</router-link>
        </p>
      </b-col>
      <!-- <b-col class="align-button" sm="2">
        <b-button class="button-submit" @click="uploadImage">Upload a folder</b-button>
      </b-col> -->

      <b-col class="align-file-input" sm="3">
        <b-form-file
          v-model="multipleImages"
          placeholder="Please choose an image/images or drop it here!"
          accept="image/jpeg, image/png"
          multiple
        ></b-form-file>
      </b-col>
      <b-col class="align-button" sm="2">
        <b-button class="button-submit" @click="uploadMultipleImages">Upload images</b-button>
      </b-col>

        <b-col class="align-file-input" sm="5">
        <b-form-file
          v-model="imageFolder"
          placeholder="Please choose an image folder or drop it here!"
          directory
          no-traverse
        ></b-form-file>
      </b-col>
      <b-col class="align-button" sm="4">
        <b-button class="button-submit" @click="uploadImageFolder">Upload image folder</b-button>
      </b-col>

    </b-row>


    <form>
      <b-row>
        <b-col cols="10">
          <b-input-group>
            <b-input-group-prepend>
              <b-input-group-text>
                <b-icon icon="search"></b-icon>
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


      <figure
        class="figure col col-md-4 col-sm-6 col-xs-12 no-drag"
        v-for="image in images"
        v-bind:key="image.id"
      >
        <img
          :src="imgSrc(image)"
          class="figure-img img-fluid rounded"
          :alt="image.id"
         @click="putIntoBox(image)" 
        />
        <b-button @click="deleteImage(image.id)">delete</b-button>
        <figcaption class="figure-caption text-center">
          {{""}}
        </figcaption>
      </figure>


    <b-row>
      <b-col md="4" sm="6" xs="12" v-for="(image, index) in images" v-bind:key="image.id">
        <router-link :to="{name: 'AnnotateImage', params: {imageId: image.id}}">
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

    <b-modal id="success-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>Upload an image successfully!</h3>
      </div>
      <b-button
          class="mt-3"
          block
          @click="$bvModal.hide('success-message-modal')"
      >Close Me
      </b-button
      >
    </b-modal>

    <b-modal id="no-image-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>Please upload an image!</h3>
      </div>
      <b-button
          class="mt-3"
          block
          @click="$bvModal.hide('no-image-message-modal')"
      >Close Me
      </b-button
      >
    </b-modal>

    <b-modal id="failed-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>Failed to upload an image!</h3>
      </div>
      <b-button
          class="mt-3"
          block
          @click="$bvModal.hide('failed-message-modal')"
      >Close Me
      </b-button
      >
    </b-modal>


  </b-container>
</template>

<script>
import {mapActions} from 'vuex'
import axios from "axios"

export default {
  name: 'ImageList',
  data() {
    return {
      images: [],
      bankName: '(loading)',
      multipleImages: [],
      imageFolder: [],
      imageFile: null,
    }
  },
  methods: {
    ...mapActions({
      listImages: 'listImages', 
      uploadImages: 'uploadImages', 
      uploadImage: 'uploadImage',
      getImages: 'getImages'
    }),
    fetchImageList() {
      this.listImages({bankId: this.$route.params.bankId})
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

    getAllImages() {
      this.getImages({bankName: this.$route.params.bankName})
          .then(res => {
            if (res.status !== 200) {
              console.log('Could not load DB => ERROR, HTTP status=' + res.status) // TODO: handle correctly
            } else {
              let data = res.data
              this.images = data.images
              this.bankName = data.bank_name
            }
          })
          .catch(err => {
            console.log(err) // TODO: handle errors properly
          })
    },

    imgSrc(image) {
      return require(image.file_url);
    },

    uploadMultipleImages() {
      if (this.multipleImages == null) {
        this.$bvModal.show('no-image-message-modal')
        return
      }

      let formData = new FormData()
      console.log(this.multipleImages)
      this.multipleImages.forEach((image) => {
        formData.append('images', image)
        formData.append('bank_name', bankName)
      })
      axios
        .post('http://localhost:5000' + "/api/upload/multiple/images", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (res.status == 200) {
            this.$bvModal.show("success-message-modal");
          } else {
            this.$bvModal.show("failed-message-modal");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    uploadImageFolder() {
      if (this.imageFolder == null) {
        this.$bvModal.show('no-image-message-modal')
        return
      }

      let formData = new FormData()
      console.log(this.imageFolder)
      this.imageFolder.forEach((image) => {
        formData.append('images', image)
      })
      // formData.append('images', this.imageFolder)
      axios
        .post('http://localhost:5000' + "/api/upload/multiple/images", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (res.status == 200) {
            this.$bvModal.show("success-message-modal");
          } else {
            this.$bvModal.show("failed-message-modal");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
  created() {
    this.fetchImageList()
    this.getAllImages()
  },
}
</script>
