<template>
  <b-container fluid>
    <div class="container">
      <b-row>
        <b-col sm="6">
          <b-form-file
            v-model="textFile"
            placeholder="Click here to choose a .txt file, then click import!"
            accept=".txt"
          ></b-form-file>
          <b-button @click="textFile = null">Reset</b-button>
          <b-button @click="readFile">Import</b-button>
        </b-col>
        <b-col sm="6">
          <form
            action="http://localhost:5000/api/image/upload"
            method="post"
            enctype="multipart/form-data"
          >
            <input type="file" name="pic" value="choose"/>
            <input type="submit" value="Upload it!" />
          </form>
          <!-- <form enctype="multipart/form-data">
            <b-form-file
              v-model="image_file"
              name="pic"
              placeholder="Please choose an image or drop it here!"
              accept="image/jpeg, image/png"
            ></b-form-file>
            <b-button @click="image_file = null">Reset</b-button>
            <b-button @click="uploadImage">upload</b-button>
          </form> -->
        </b-col>
      </b-row>

      <b-row>
        <b-col sm="2">
          <button type="button" class="btn btn-primary">Select words</button>
        </b-col>
        <b-col sm="4">
          <b-form-textarea
            id="textarea-auto-height"
            v-model="text"
            placeholder="Auto height textarea"
            rows="3"
            max-rows="8"
          ></b-form-textarea>
        </b-col>
        <b-col sm="6">
          <img
            :src="imageBox"
            class="figure-img img-fluid rounded"
            :alt="error"
          />
          <div style='text-align:center'>
            <button type="button" class="btn btn-primary">Select regions</button>
          </div>
        </b-col>
      </b-row>
      <div style='text-align:center'>
        <button type="button" class="btn btn-primary">Export as PDF</button>
      </div>
    </div>

    <h2>All your uploaded images will be displayed here</h2>
    <figure
      class="figure col col-md-4 col-sm-6 col-xs-12 no-drag"
      v-for="image in newImages"
      v-bind:key="image.id"
    >
      <img
        :src="imgSrc(image)"
        class="figure-img img-fluid rounded"
        :alt="image.id"
        @click="putIntoBox(image)"
      />
      <figcaption class="figure-caption text-center">
        {{ image.imageName }}
      </figcaption>
    </figure>

    <b-modal id="success-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>Upload an image successfully!</h3>
      </div>
      <b-button
        class="mt-3"
        block
        @click="$bvModal.hide('success-message-modal')"
        >Close Me</b-button
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
        >Close Me</b-button
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
        >Close Me</b-button
      >
    </b-modal>
  </b-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  data() {
    return {
      // Text area
      text: "",
      // The .txt file uploaded
      textFile: null,
      // Save all the images info that user uploaded
      newImages: [],
      // The image uploaded
      image_file: null,
      // This may be deleted
      imageState: null,
      // Box to display the image to be annotated
      imageBox: null,
    };
  },
  methods: {
    // Handle upload image feature, still have problems
    uploadImage() {
      if (this.image_file == null) {
        this.$bvModal.show("no-image-message-modal");
        return;
      }
      let image = {
        image_bank: "butterfly",
        image_file: this.image_file,
      };
      axios
        .post(this.$hostname + "/api/image/upload", image)
        .then((res) => {
          console.log(res);
          console.log(res.data);
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
    // Handle text import feature
    readFile() {
      var fileReader = new FileReader();
      fileReader.readAsText(this.textFile);
      fileReader.onload = () => {
        this.text = fileReader.result;
      };
    },
    // display all the images the user uploaded
    getAllImages() {
      console.log("enter getAllImages");
      axios
        .get(this.$hostname + "/api/image/getImage")
        .then((res) => {
          console.log(res);
          let data = res.data;
          this.newImages = data.images;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    imgSrc(image) {
      return require("../../../website/images/source_images/" +
        image.imageName);
    },
    putIntoBox(image) {
      this.imageBox = require("../../../website/images/source_images/" +
        image.imageName);
    },
  },
  created() {
    this.getAllImages();
  },
};
</script>