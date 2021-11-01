<template>
  <div>
    <div>
      <b-button-toolbar :justify="true">
        <b-button
          @click="getPrevious()"
          variant="outline-primary"
          :disabled="noPrevious"
          >Previous</b-button
        >

        <b-button
          @click="getNext()"
          variant="outline-primary"
          :v-show="noNext"
          >next</b-button
        >
      </b-button-toolbar>

      <br />
      <b-row>
        <b-col class="textbox-area" sm="1">
          <b-button class="button-submit">Select words</b-button>
        </b-col>

        <b-col class="textbox-area" sm="3">
          <b-form-textarea
            id="textarea-auto-height"
            v-model="text"
            placeholder="Auto height textarea"
            rows="10"
            max-rows="8"
          ></b-form-textarea>
        </b-col>

        <b-col sm="8">
          <div class="card" style="width: 40rem">
            <img
              :src="imageBox"
              class="card-img-top figure-img img-fluid rounded"
              alt="Currently no image in this area, please choose one from the image you uploaded."
              style="width: auto; height: 380px"
            />

            <div class="card-body" style="text-align: center">
              <h5 class="card-text">{{ imageDescription }}</h5>
              <b-button class="button-submit" type="button">
                Select regions
              </b-button>
            </div>
          </div>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  name: "AnnotateImage",
  data() {
    return {
      // Text area
      text: "",
      // Box to display the image to be annotated
      imageBox:
        "",
      // The description of the image user selected
      imageDescription: "",
      noPrevious: false,
      noNext: false,
    };
  },
  methods: {
    ...mapActions({ nextImage: 'nextImage', previousImage: 'previousImage' , getImage: 'getImage'}),
    hasPrevious() {
      this.previousImage({ imageId: this.$route.params.imageId }).then(_ => {
        return true
      }).catch(error => {
        return false
      });
    },
    hasNext() {
      this.nextImage({ imageId: this.$route.params.imageId }).then(_ => {
        return true
      }).catch(error => {
        return false
      });
    },
    getImageInfo() {
      this.getImage({ imageId: this.$route.params.imageId }).then(res => {
        const image = res.data.image
        this.text = image.description
        this.imageBox = image.url
      }).catch(error => {
        console.log(error)
      })
    },
    getPrevious() {
      this.previousImage({ imageId: this.$route.params.imageId }).then(res => {
        const previousImage = res.data.image
        console.log(previousImage)
        this.$router.push({ name: 'AnnotateImage', params: {imageId: previousImage.id} })
      }).catch(error => {
        console.log(error)
      });
    },

    getNext() {
      this.nextImage({ imageId: this.$route.params.imageId }).then(res => {
        const nextImage = res.data.image
        console.log(nextImage)
        this.$router.push({ name: 'AnnotateImage', params: {imageId: nextImage.id} })
        
      }).catch(error => {
        console.log(error)
      });
    },
  },
  watch: {
    $route(to, from) {
      this.getImageInfo()
    }
  },
  created() {
    this.getImageInfo()
  }
};
</script>

<style>
.col-sm-1.align-button {
  padding-left: 0;
}

.col-sm-5.align-file-input {
  padding-right: 0;
}

.button-submit.btn-secondary {
  color: black;
  background-color: #e9ecef;
}

/* layout of the "select words" button */
.textbox-area.col-sm-1 {
  padding: 0;
  margin-top: 4rem;
}
</style>