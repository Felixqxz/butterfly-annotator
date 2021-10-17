<template>
  <b-container fluid>
    <div class="container">
      <b-row>
        <b-col sm="6">
          <b-form-file
            v-model="textFile"
            placeholder="Please choose a .txt file!"
            accept=".txt"
          ></b-form-file>
          <b-button @click="textFile = null">Reset</b-button>
          <b-button @click="readFile">Import</b-button>
        </b-col>
        <b-col sm="6">
          <form enctype="multipart/form-data">
            <b-form-file
              v-model="image_file"
              name="pic"
              placeholder="Please choose a image or drop it here!"
              accept="image/jpeg, image/png"
            ></b-form-file>
            <b-button @click="image_file = null">Reset</b-button>
            <b-button @click="uploadImage">upload</b-button>
          </form>
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
        <figure
          class="figure col col-md-4 col-sm-6 col-xs-12 no-drag"
          v-for="image in images"
          v-bind:key="image.id"
        >
          <img
            :src="image.url"
            class="figure-img img-fluid rounded"
            :alt="image.id"
          />
          <figcaption class="figure-caption text-center">butterfly</figcaption>
        </figure>
      </b-row>
    </div>

    <form action="http://localhost:5000/api/image/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="pic">
      <input type="submit" value="Upload a file">
      <!-- <b-form-file name="file_upload[]" :multiple="true" :file-name-formatter="formatAssetUpload" no-drop placeholder="Click to choose"></b-form-file> -->
    </form>

    <!-- <div>
      <b-button v-b-modal.modal-prevent-closing>Upload image</b-button>
      <b-modal
        id="modal-prevent-closing"
        ref="modal"
        title="Upload Your Image"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleOk"
      >
        <form ref="form" @submit.stop.prevent="handleSubmit">
          <b-form-group
            label="Image"
            label-for="image-input"
            invalid-feedback="If you want to upload, you must choose an image first!"
            :state="imageState"
          >
            <b-form-file
              id="image-input"
              v-model="image_file"
              class="mt-3"
              placeholder="Choose a image or drop it here!"
              accept="image/jpeg, image/png"
              :state="imageState"
              required
            ></b-form-file>
          </b-form-group>
        </form>
      </b-modal>
    </div> -->

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
      // This may be deleted
      images: [],
      // The image uploaded
      image_file: null,
      // This may be deleted
      imageState: null,
    };
  },
  methods: {
    getImages() {
      axios
        .get(this.$hostname + "/api/images")
        .then((res) => {
          let data = res.data
          this.images = data.images
        })
        .catch((err) => {
          console.log(err)
        });
    },
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
      console.log(this.image_file)
      console.log(image)
      axios
        .post(this.$hostname + "/api/image/upload", image)
        .then((res) => {
          console.log(res)
          console.log(res.data)
          if (res.status == 200) {
            this.$bvModal.show("success-message-modal")
          } else {
            this.$bvModal.show("failed-message-modal")
          }
        })
        .catch((err) => {
          console.log(err)
        });
    },
    // Handle text import feature
    readFile() {
      var fileReader = new FileReader()
      fileReader.readAsText(this.textFile)
      fileReader.onload = () => {
        this.text = fileReader.result
      };
    },
    getCount() {
      console.log('enter')
      axios
        .get(this.$hostname + "/api/image/getImage")
        .then((res) => {
          console.log(res)
        })
        .catch((err) => {
          console.log(err)
        });
    }
    // checkFormValidity() {
    //   const valid = this.$refs.form.checkValidity();
    //   this.imageState = valid;
    //   return valid;
    // },
    // resetModal() {
    //   this.image_file = "";
    //   this.imageState = null;
    // },
    // handleOk(bvModalEvt) {
    //   // Prevent modal from closing
    //   bvModalEvt.preventDefault();
    //   // Trigger submit handler
    //   this.handleSubmit();
    // },
    // handleSubmit() {
    //   // Exit when the form isn't valid
    //   if (!this.checkFormValidity()) {
    //     return;
    //   }
    //   console.log(this.image_file)
    //   // Hide the modal manually
    //   this.$nextTick(() => {
    //     this.$bvModal.hide("modal-prevent-closing");
    //   });
    // },
  },
  created() {
    this.getImages()
    this.getCount()
  },
};
</script>