<template>
  <div>
    <div>

      <b-row>
        <b-col class="align-file-input" sm="5">
          <b-form-file
              v-model="textFile"
              placeholder="Click here to choose a .txt file, then click import!"
              accept=".txt"
          ></b-form-file>
        </b-col>

        <b-col class="align-button" sm="1">
          <b-button class="button-submit" @click="readFile">Import</b-button>
        </b-col>

        <b-col class="align-file-input" sm="5">
          <b-form-file
              v-model="imageFile"
              placeholder="Please choose an image or drop it here!"
              accept="image/jpeg, image/png"
          ></b-form-file>
        </b-col>

        <b-col class="align-button" sm="1">
          <b-button class="button-submit" @click="uploadImage">Upload</b-button>
        </b-col>
      </b-row>
      <br>
      <b-row>
        <b-col class="textbox-area" sm="1">
          <b-button class="button-submit">Select words</b-button>
        </b-col>

        <b-col class="textbox-area" sm="5">
          <b-form-textarea
              id="textarea-auto-height"
              v-model="text"
              placeholder="Auto height textarea"
              rows="10"
              max-rows="8"
          ></b-form-textarea>
        </b-col>

        <b-col sm="6">
          <div class="card" style="width: 32rem">
            <img
                :src="imageBox"
                class="card-img-top figure-img img-fluid rounded"
                alt="Currently no image in this area, please choose one from the image you uploaded."
                style="width: auto; height: 380px;"
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

      <div style="text-align: center">
        <b-button id="button-export" class="button-submit" type="button" size="lg">Export as PDF</b-button>
      </div>

    </div>

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
      >Close Me
      </b-button
      >
    </b-modal>

    <b-modal id="success-textFile-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>import file successfully!</h3>
      </div>
      <b-button
          class="mt-3"
          block
          @click="$bvModal.hide('success-textFile-message-modal')"
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

    <b-modal id="failed-textFile-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>Failed to upload an image!</h3>
      </div>

      <b-button
          class="mt-3"
          block
          @click="$bvModal.hide('failed-textFile-message-modal')"
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

    <b-modal id="no-textFile-message-modal" hide-footer>
      <div class="d-block text-center">
        <h3>Please choose a .txt file!</h3>
      </div>
      <b-button
          class="mt-3"
          block
          @click="$bvModal.hide('no-textFile-message-modal')"
      >Close Me
      </b-button
      >
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AnnotateImage',
  data() {
    return {
      // Text area
      text: '',
      // The .txt file uploaded
      textFile: null,
      // Save all the images info that user uploaded
      newImages: [],
      // The image uploaded
      imageFile: null,
      // This may be deleted
      imageState: null,
      // Box to display the image to be annotated
      imageBox:
          'https://cdn.mos.cms.futurecdn.net/MutKXr3Z2za46Zdi3XM3BM-1200-80.jpg',
      // The description of the image user selected
      imageDescription:
          'This is an example image, please click one you uploaded!',
    }
  },
  methods: {
    // Handle upload image feature, still have problems
    uploadImage() {
      if (this.imageFile == null) {
        this.$bvModal.show('no-image-message-modal')
        return
      }

      let formData = new FormData()
      formData.append('imgFile', this.imageFile)
      axios.post(this.$hostname + '/api/image/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }).then(res => {
        if (res.status === 200) {
          this.$bvModal.show('success-message-modal')
        } else {
          this.$bvModal.show('failed-message-modal')
        }
      }).catch(err => {
        console.log(err)
      })
      this.getAllImages();
    },
    // Handle text import feature
    // text is defined in data() {}
    readFile() {
      if (this.textFile == null) {
        this.$bvModal.show('no-textFile-message-modal')
        return
      }
      let fileReader = new FileReader()
      fileReader.readAsText(this.textFile)
      fileReader.onload = () => {
        this.text = fileReader.result
      }

      let formData = new FormData()
      formData.append('txtFile', this.textFile)

      axios.post(this.$hostname + '/api/description/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }).then(res => {
        if (res.status === 200) {
          this.$bvModal.show('success-textFile-message-modal')
        } else {
          this.$bvModal.show('failed-textFile-message-modal')
        }
      }).catch(err => {
        console.log(err)
      })
    },
    //display all the images the user uploaded
    getAllImages() {
      axios
        .get(this.$hostname + "/api/image/getImage")
        .then((res) => {
          let data = res.data;
          this.newImages = data.images;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    imgSrc(image) {
      return require('../../../website/static/source_images/' +
          image.imageName)
    },
    putIntoBox(image) {
      this.imageBox = require('../../../website/static/source_images/' +
          image.imageName)
      this.imageDescription = image.imageName.split('.')[0]
    },
  },
  created() {
    this.getAllImages()
  },
}
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
  background-color: #E9ECEF;
}

.textbox-area.col-sm-1 {
  padding: 0;
  margin-top: 70px;
}

#button-export {
  margin-top: 40px;
}
</style>