<template>
  <b-container fluid>
    <div class="container">
      <b-row>
        <b-col sm="6">
          <b-form-file
            v-model="textFile"
            ref="txt-file"
            name="txt"
            placeholder="Please choose a .txt file!"
            accept=".txt"
            enctype="multipart/form-data"
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

    <b-modal id="success-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>Upload an image/text successfully!</h3>
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
        <h3>Failed to upload an image/text!</h3>
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
        <h3>Please upload an image/text!</h3>
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
      // console.log(this.image_file)
      // console.log(image)

      let formData = new FormData()
      formData.append('imgFile', this.image_file)

      axios({
              method: 'post',
              url: this.$hostname + "/api/image/upload",
              data: {
                formData
              },
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }).then((res) => {

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
    //text is defined in data() {}
    readFile() {
      var fileReader = new FileReader()
      fileReader.readAsText(this.textFile)
      fileReader.onload = () => {
        this.text = fileReader.result
      };

      let formData = new FormData()
      formData.append('txtFile', this.textFile)

      for (var key of formData.keys()) {
        console.log(key);
        console.log(formData.get(key));
      }

      axios
        .post(this.$hostname + "/api/description/upload", formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        ).then((res) => {

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

  },
  created() {
    this.getImages()
    this.getCount()
  },
};
</script>