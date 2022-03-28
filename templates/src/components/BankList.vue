<template>
  <b-container @dragover.prevent="beginDrag">
    <b-row class="justify-content-center">
      <b-col cols="12">
        <h2 class="page-title">
          Your banks
          <b-button 
            @click="showUpload = true"
            class="upload-button" 
            variant="outline-primary"
            v-tippy="{arrow: true, arrowType: 'round', theme: 'google'}"
            content="You can also drag and drop archives to this page to upload them!">
            <b-icon-cloud-upload/>
          </b-button>
        </h2>
      </b-col>
    </b-row>
    <div class="bank-list">
      <b-row class="justify-content-center" v-for="bank in availableBanks" v-bind:key="bank.id">
        <b-col cols="12">
          <router-link :to="'/bank/' + bank.id">
            <b-card class="card-hover bank-list-card">
              <b-card-title>
                {{ bank.name }}
              </b-card-title>
              <b-card-text class="text-muted">
                {{ bank.description }}
              </b-card-text>
            </b-card>
          </router-link>
        </b-col>
      </b-row>
    </div>
    <div :class="'upload-section' + (showUpload ? ' upload-section-shown' : '')" @dragleave="stopDrag">
      <!-- Hover shadow -->
      <div :class="'upload-shadow' + (showUpload ? ' upload-shadow-shown' : '')">
      </div>
      <!-- The content itself -->
      <div class="upload-modal" @drop="chooseFile">
        <b-container fluid>
          <b-row class="justify-content-end" style="margin-bottom: 1em;">
            <b-col cols="1">
              <!-- 'Close' button -->
              <b-button variant="outline-secondary" @click="showUpload = false"><b-icon-x-circle/></b-button>
            </b-col>
          </b-row>
          <b-row class="justify-content-center">
            <b-col cols="12">
              <div class="upload-input" v-if="bankFile === null">
                <!-- Fake file input to trigger browsing -->
                <input type="file" accept=".zip" id="file-upload" class="hidden-upload" ref="hidden-upload" @change="checkFiles">
                <b-button @click="$refs['hidden-upload'].click()" variant="primary" class="cloud-upload-button">
                  <b-icon-file-earmark-arrow-up/>
                </b-button>
                <p class="no-drag suggest-drag-text">Drop your zip file containing your bank</p>
              </div>
              <div class="upload-input" v-else>
                <p>You chose the file {{ bankFile.name }}.
                <br><a href="javascript:void(0)" style="font-size: 80%;" @click="clearSelection">Clear selection</a></p>
                <waiting-button
                  style="font-size: 1em;" 
                  :startAction="uploadBank"
                  :loading="uploadProgress !== -1"
                  :progressPercentage="uploadProgress">Upload</waiting-button>
              </div>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </b-container>
</template>

<script>
import {mapActions} from 'vuex'
import handleError from '../errors/handler'
import WaitingButton from './WaitingButton'

export default {
  name: 'BankList',
  data() {
    return {
      availableBanks: [],
      showUpload: false,
      bankFile: null,
      uploadProgress: -1,
    }
  },
  components: {
    WaitingButton
  },
  methods: {
    ...mapActions({listBanks: 'listBanks', uploadBankRemote: 'uploadBank'}),
    updateBanks() {
      this.listBanks().then(req => this.availableBanks = req.data)
          .catch(err => handleError(this.$bvToast, 'Cannot list banks',
              `Cause: ${err.response.data.message}`))
    },
    beginDrag(e) {
      e.stopPropagation()
      const transfer = e.dataTransfer
      this.showUpload = transfer.types && transfer.types.indexOf && transfer.types.indexOf('Files') !== -1
      e.dataTransfer.effectAllowed = 'all'
      e.dataTransfer.dropEffect = 'all'
    },
    stopDrag(e) {
      this.showUpload = false
    },
    chooseFile(e) {
      e.preventDefault()
      const files = e.dataTransfer.files
      // no files or not a zip archive
      if (files.length === 0 || !files[0].name.endsWith('.zip')) {
        return
      }
      // accept the file
      this.bankFile = files[0]
    },
    checkFiles(e) {
      if (this.$refs['hidden-upload'].files.length < 1) {
        return
      }
      const file = this.$refs['hidden-upload'].files[0]
      this.bankFile = file  
    },
    clearSelection() {
      this.bankFile = null
    },
    uploadBank() {
      if (this.bankFile === null) {
        handleError(this.$bvToast, 'Cannot upload file', 'No file has been selected.')
        return
      }
      
      // progress handler
      const progressHandler = e => {
        this.uploadProgress = Math.floor(e.loaded * 100 / e.total)
      }
      // prepare file
      const formData = new FormData()
      formData.append('file', this.bankFile)
      // upload
      this.uploadBankRemote({formData, progressHandler}).then(res => {
        this.$bvToast.toast(res.data.message, {
          title: 'Successfully uploaded bank!',
          variant: 'success',
          solid: true,
        })
        // clear state
        this.showUpload = false
        this.bankFile = null
        this.updateBanks()
        this.loading = false
        this.uploadProgress = -1
      }).catch(e => handleError(this.$bvToast, 'Could not upload bank', `Cause: ${e.response.data.message}`))
    },
  },
  created() {
    this.updateBanks()
  },
}
</script>
<style scoped>
.bank-list-card {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.upload-button {
  margin-left: 1em;
}

.upload-section {
  height: 100vh;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  visibility: hidden;
}

.upload-shadow-shown {
  opacity: 0.65 !important;
  transition: 200ms opacity;
}

.upload-section-shown {
  visibility: initial !important;
}

.upload-shadow {
  height: 100vh;
  width: 100%;
  background-color: rgb(0, 0, 0);
  opacity: 0;
  position: fixed;
}

.upload-modal {
  position: relative;
  width: 75%;
  border-radius: 1rem;
  background-color: white;
  margin: 5em;
  padding: 1em 1em 1.5em 1em;
  margin-left: auto;
  margin-right: auto;
}

.hidden-upload {
  display: none;
}

.upload-input {
  border-style: dashed;
  border-color: rgba(0, 0, 0, 0.3);
  width: 100%;
  height: 10em;
  text-align: center;
  padding-top: 2em;
}

.cloud-upload-button {
  width: 6rem;
  font-size: 2em;
}

.cloud-upload-button, .cloud-upload-button:hover {
  border: none;
}

.suggest-drag-text {
  color: gray;
  margin-top: 1em;
}
</style>
