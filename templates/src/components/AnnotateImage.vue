<template>
  <div>
    <div>
      <p>
        <router-link
          :to="{
            name: 'ImageList',
            params: { bankName: $route.params.bankName },
          }"
          >Return to the list of banks</router-link
        >
      </p>
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
          :disabled="noNext"
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
            placeholder="Description"
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
              style="width: auto; height: auto"
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
      imageBox: "",
      // The description of the image user selected
      imageDescription: "",
      noPrevious: false,
      noNext: false,
    };
  },
  methods: {
    ...mapActions({
      nextImage: "nextImage",
      previousImage: "previousImage",
      getImage: "getImage",
    }),
    imgSrc(image) {
      let arr = image.split("/");
      let image_name = arr[arr.length - 1];
      this.imageBox = require(`../../../website/static/source_images/${image_name}`);
    },
    getImageInfo() {
      this.getImage({ imageId: this.$route.params.imageId })
        .then((res) => {
          const image = res.data.image;
          this.text = image.description;

          let arr = image.url.split("/");
          let image_name = arr[arr.length - 1];
          this.imageBox = require("../../../website/static/source_images/" +
            image_name);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getPrevious() {
      const t = this;
      this.previousImage({ imageId: this.$route.params.imageId }).then(
        (res) => {
          if (res.data.status === 200) {
            const previousImage = res.data.image;
            t.$router.push({
              name: "AnnotateImage",
              params: {
                bankName: this.$route.params.bankName,
                imageId: previousImage.id,
              },
            });
          }
        }
      );
    },

    getNext() {
      const t = this;
      this.nextImage({ imageId: this.$route.params.imageId }).then((res) => {
        if (res.data.status === 200) {
          const nextImage = res.data.image;
          t.$router.push({
            name: "AnnotateImage",
            params: {
              bankName: this.$route.params.bankName,
              imageId: nextImage.id,
            },
          });
        }
      });
    },

    updatePage() {
      const t = this;
      this.getImageInfo();
      this.nextImage({ imageId: this.$route.params.imageId }).then((res) => {
        if (res.data.status === 404) {
          t.noNext = true;
        }
      });
      this.previousImage({ imageId: this.$route.params.imageId }).then(
        (res) => {
          if (res.data.status === 404) {
            t.noPrevious = true;
          }
        }
      );
    },
  },
  watch: {
    $route(to, from) {
      this.noNext = false;
      this.noPrevious = false;
      this.updatePage();
    },
  },
  created() {
    this.updatePage();
  },
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