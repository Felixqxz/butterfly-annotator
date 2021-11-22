<template>
  <div>
    <div class="profile-picture"
         :style="'background-image: url(' + picture + ')'">
    </div>
    <p v-if="Boolean(editable)" class="text-center" @click="openUploadModal()"><a href="#">Upload a new picture</a></p>
    <b-modal size="lg" title="New avatar" id="upload-picture" hide-footer>
      <b-row class="mb-2">
        <b-col cols="12">
          <b-form-file
            v-model="pictureToUpload"
            :state="Boolean(pictureToUpload)"
            accept="image/jpeg"
            placeholder="Upload a new profile picture (.jpg)"
            drop-placeholder="Drop your file here">
          </b-form-file>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="6" xs="12">
          <b-button variant="primary" class="mb-2" @click="submitImage()" :disabled="!pictureToUpload">
            <span class="mr-2">OK</span><b-icon-upload></b-icon-upload>
          </b-button>
        </b-col>
        <b-col md="6" xs="12" class="d-flex justify-content-md-end">
          <b-button variant="danger" @click="cancel()">Cancel</b-button>
        </b-col>
      </b-row>
    </b-modal>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import handleError from '../errors/handler'

export default {
  name: 'ProfilePicture',
  data() {
    return {
      pictureToUpload: null,
    }
  },
  props: {
    picture: {
      required: true,
      type: String,
    },
    editable: {
      required: false,
      type: Boolean,
    },
  },
  methods: {
    ...mapActions({ uploadProfilePicture: 'uploadProfilePicture' }),
    openUploadModal() {
      this.$bvModal.show('upload-picture')
    },
    cancel() {
      this.pictureToUpload = null
      this.$bvModal.hide('upload-picture')
    },
    submitImage() {
      this.$bvModal.hide('upload-picture')
      const formData = new FormData()
      formData.append('file', this.pictureToUpload, this.pictureToUpload.name)
      this.uploadProfilePicture({formData}).catch(e => handleError(this.$bvToast, 'Could not upload picture',
          `Cause ${e.response.data.message}`))
    },
  },
}
</script>

<style scoped>
.profile-picture {
  height: 20em;
  background-size: cover;
  background: transparent no-repeat center;
  border-radius: 100%;
}
</style>
