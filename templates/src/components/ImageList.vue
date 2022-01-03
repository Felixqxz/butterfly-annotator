<template>
  <b-container>
    <h2 class="page-title">
      Bank: {{ bankName }}
      <b-button variant="secondary" v-b-modal.settings-modal>
        <b-icon-gear/>
      </b-button>
      <b-modal id="settings-modal" title="Settings" hide-footer>
        <b-button variant="danger" @click="deleteBank" :disabled="currentAccess >= 90">
          Delete bank
        </b-button>
      </b-modal>
    </h2>
    <b-row>
      <b-col>
        <p>
          <router-link to="/">Return to the list of banks</router-link>
        </p>
      </b-col>
    </b-row>
    <b-tabs justified>
      <b-tab title="Images" active>
        <form>
          <b-row>
            <b-col cols="12" class="mt-2">
              <b-input-group @keydown.enter.prevent="">
                <b-input-group-prepend>
                  <b-input-group-text>
                    <b-icon-search></b-icon-search>
                  </b-input-group-text>
                </b-input-group-prepend>
                <input type="text" class="form-control" placeholder="Search..." v-model="searchText"/>
              </b-input-group>
            </b-col>
          </b-row>
        </form>
        <b-row>
          <b-col md="4" sm="6" xs="12" v-for="image in imagesToShow" v-bind:key="image.id">
            <router-link :to="'/annotate/' + image.id">
              <!-- no-body to put custom body -->
              <b-card class="card-hover no-drag image-to-annotate fade-in-with-style" no-body>
                <div class="image-hover-container">
                  <img :src="$hostname + '/api/' + image.url" class="card-img-top image-hover image-in-place"
                       :alt=image.id />
                  <div v-if="Boolean(image.lastEditor)" 
                    class="last-editor" 
                    :style="'background-image: url(' + $hostname + '/api/profile-picture/' + image.lastEditor.username + ')'"
                    v-tippy="{content: `<em>${image.lastEditor.username}</em> last annotated this`, arrow: true, arrowType: 'round', theme: 'google'}"/>
                </div>
                <b-card-body class="row justify-content-between align-items-center">
                  <b-col cols="12">
                    <b-card-text>{{ image.fullDescription.substring(0, 120) }}...</b-card-text>
                  </b-col>
                </b-card-body>
              </b-card>
            </router-link>
          </b-col>
        </b-row>
      </b-tab>
      <!-- Accesses tab -->
      <b-tab title="Accesses">
        <b-row :v-show="hasPermissionToAdd()">
          <b-col cols="12">
            <b-button v-b-modal.add variant="primary" class="mb-2 mt-2">Add user</b-button>
          </b-col>

          <b-modal id="add" ref="add-modal" title="Add user" hide-footer>
            <b-form autocomplete="off">
              <h4 class="text-center">Add a user to this group</h4>
              <b-form-group id="user-add-input" label-for="target-user">
                <label>Username:</label>
                <b-form-input id="target-user" name="target-user" v-model="targetUser">
                </b-form-input>
              </b-form-group>
              <b-form-group>
                <b-form-select v-model="selectedLevel" :options="permissionOptions"></b-form-select>
              </b-form-group>
              <b-button @click="addUser()">
                Add
              </b-button>
            </b-form>
          </b-modal>
        </b-row>
        <b-row v-for="access in userAccesses" v-bind:key="access.username" class="mb-2 justify-content-center">
          <b-col cols="12">
            <b-card>
              {{ access.username }}
              <permission-badge :color-variant="levelToVariant(access.level)"
                                :permission-title="levelToTitle(access.level)"></permission-badge>
              <b-button variant="danger" @click="removeUser(access.username)" class="float-right remove-user-button"><b-icon-x-circle></b-icon-x-circle></b-button>
            </b-card>
          </b-col>
        </b-row>
      </b-tab>
      <template #tabs-end>
        <b-nav-item href="#" role="presentation" @click="downloadJson()"><b-icon-download class="pr-2"></b-icon-download>Export to JSON</b-nav-item>
      </template>
    </b-tabs>
  </b-container>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import PermissionBadge from './PermissionBadge'
import handleError from '../errors/handler'

export default {
  name: 'ImageList',
  components: {
    PermissionBadge
  },
  data() {
    return {
      images: [],
      bankName: '(loading)',
      userAccesses: [],
      currentAccess: null,
      selectedLevel: null,
      permissionOptions: [],
      targetUser: null,
      searchText: '',
    }
  },
  computed: {
    ...mapGetters({ userInfo: 'currentUser' }),
    imagesToShow() {
      const search = this.searchText.trim()
      if (search) {
        return this.images.filter(image => image.fullDescription.toLowerCase().includes(search.toLowerCase()))
      } else {
        return this.images
      }
    },
  },
  methods: {
    ...mapActions({
      listImages: 'listImages',
      listAccesses: 'listAccesses',
      requestPermission: 'requestPermission',
      requestJson: 'requestBankJson',
      requestDeleteBank: 'deleteBank',
    }),
    hasPermissionToAdd() {
      return this.currentAccess ? this.currentAccess >= 70 : false
    },
    levelToTitle(level) {
      if (level === 0) {
        return 'Viewer'
      } else if (level === 50) {
        return 'Editor'
      } else if (level === 70) {
        return 'Moderator'
      } else if (level === 90) {
        return 'Admin'
      } else if (level === 100) {
        return 'Super Admin'
      } else {
        return 'Invalid level'
      }
    },
    levelToVariant(level) {
      if (level === 0) {
        return 'light'
      } else if (level === 50) {
        return 'primary'
      } else if (level === 70) {
        return 'success'
      } else if (level === 90) {
        return 'danger'
      } else if (level === 100) {
        return 'danger'
      } else {
        return 'secondary'
      }
    },
    fetchImageList() {
      this.listImages({bankId: this.$route.params.bankId})
        .then(res => {
          let data = res.data
          this.images = data.images
          this.bankName = data.bankName
        })
        .catch(err => {
          handleError(this.$bvToast, 'Cannot load image list', `Cause ${err.response.data.message}`)
        })
    },
    relistAccesses() {
      this.listAccesses({bankId: this.$route.params.bankId}).then(res => {
        this.userAccesses = res.data.users
        this.userAccesses.sort((b, a) => a.level - b.level)
        for (let i = 0; i < res.data.users.length; ++i) {
          const access = res.data.users[i]
          if (access.username === this.userInfo.username) {
            this.currentAccess = access
            if (this.currentAccess.level >= 70) {
              this.permissionOptions = ['Visitor', 'Editor', 'Moderator']
            }
            if (this.currentAccess.level >= 90) {
              this.permissionOptions.push('Admin')
            }
            break
          }
        }
      }).catch(e => handleError(this.$bvToast, 'Cannot load accesses', `Cause ${e.response.data.message}`))
    },
    addUser() {
      const targetUser = this.targetUser
      let level = null
      if (this.selectedLevel === 'Visitor') {
        level = 0
      } else if (this.selectedLevel === 'Editor') {
        level = 50
      } else if (this.selectedLevel === 'Moderator') {
        level = 70
      } else if (this.selectedLevel === 'Admin') {
        level = 90
      }
      this.$refs['add-modal'].hide()
      const bankId = this.$route.params.bankId
      this.requestPermission({targetUser, level, bankId}).then(_ => {
        this.relistAccesses()
      }).catch(e => handleError(this.$bvToast, 'Cannot add user', `Cause: ${e.response.data.message}`))
    },
    removeUser(username) {
      const targetUser = username
      const level = -1
      const bankId = this.$route.params.bankId
      this.requestPermission({targetUser, level, bankId}).then(_ => {
        this.relistAccesses()
      }).catch(e => handleError(this.$bvToast, 'Cannot remove user', `Cause: ${e.response.data.message}`))
    },
    downloadJson() {
      this.requestJson({bankId: this.$route.params.bankId}).then(res => {
        const blob = new Blob([JSON.stringify(res.data, null, 2)], { type: 'application/json' })
        const a = document.createElement('a')
        a.href = URL.createObjectURL(blob)
        a.download = 'bank.json'
        a.click()
        URL.revokeObjectURL(a.href)
      })
    },
    deleteBank() {
      this.requestDeleteBank({bankId: this.$route.params.bankId}).then(res => {
        this.$router.push({'path': '/'})
        this.$bvToast.toast('Successfully deleted bank', {
          title: 'Deleted ' + this.bankName,
          variant: 'success',
          solid: true,
        })
      }).catch(e => handleError(this.$bvToast, 'Could not delete bank', `Cause: ${e.response.data.message}`))
    },
  },
  created() {
    this.fetchImageList()
    this.relistAccesses()
  },
}
</script>
<style scoped>
.image-in-place {
  object-fit: cover;
  max-width:100%;
  max-height:100%;
  z-index: -1;
}

.image-hover-container {
  position: relative;
  overflow: hidden;
  height: 12em;
}

.image-hover {
  transform: scale(1.0);
  transform-origin: center;
  transition: 400ms transform;
}

.image-hover:hover {
  transform: scale(1.2);
  transform-origin: center;
}

.image-to-annotate {
  margin-top: 1em;
  margin-bottom: 1em;
}

.remove-user-button {
  padding-bottom: 0.2rem;
  padding-top: 0.2rem;
  padding-left: 0.3rem;
  padding-right: 0.3rem;
}

.last-editor {
  position: absolute;
  z-index: 3;
  right: 0;
  bottom: 0;
  width: 3em;
  height: 3em;
  border-radius: 100%;
  background-position: center;
  background-size: cover;
  margin: 1em;
}
</style>