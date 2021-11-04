<template>
  <b-container>
    <h2 class="page-title">Bank: {{ bankName }}</h2>
    <b-row>
      <b-col>
        <p>
          <router-link to="/">Return to the list of banks</router-link>
        </p>
      </b-col>
    </b-row>
    <b-tabs>
      <b-tab title="Images" active>
        <form>
          <b-row>
            <b-col cols="10">
              <b-input-group>
                <b-input-group-prepend>
                  <b-input-group-text>
                    <ion-icon name="search-outline"></ion-icon>
                  </b-input-group-text>
                </b-input-group-prepend>
                <input type="text" class="form-control" placeholder="Search..."/>
              </b-input-group>
            </b-col>
            <b-col cols="2">
              <!-- sort by: + options (dropdown menu?) TODO -->
            </b-col>
          </b-row>
        </form>
        <b-row>
          <b-col md="4" sm="6" xs="12" v-for="(image, index) in images" v-bind:key="image.id">
            <router-link :to="'/annotate/' + image.id">
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
      </b-tab>
      <!-- Accesses tab -->
      <b-tab title="Accesses">
        <b-row :v-show="hasPermissionToAdd()">
          <b-col cols="6">
            <b-button v-b-modal.add variant="primary">Add user</b-button>
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
        <b-card v-for="access in userAccesses" v-bind:key="access.username">
          {{ access.username }}
          <permission-badge :color-variant="levelToVariant(access.level)"
                            :permission-title="levelToTitle(access.level)"></permission-badge>
          <b-button variant="danger" @click="removeUser(access.username)" class="float-right"><ion-icon name="close-circle-outline"></ion-icon></b-button>
        </b-card>
      </b-tab>
    </b-tabs>
  </b-container>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import PermissionBadge from './PermissionBadge'

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
    }
  },
  computed: {
    ...mapGetters({ userInfo: 'currentUser' })
  },
  methods: {
    ...mapActions({listImages: 'listImages', listAccesses: 'listAccesses', requestPermission: 'requestPermission'}),
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
    relistAccesses() {
      this.listAccesses({bankId: this.$route.params.bankId}).then(res => {
        this.userAccesses = res.data.users
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
      }).catch(e => console.log(e))
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
      console.log(bankId)
      this.requestPermission({targetUser, level, bankId}).then(_ => {
        this.relistAccesses()
      }).catch(e => {
        console.log('could not add access: ' + e) // TODO: handle errors correctly
      })
    },
    removeUser(username) {
      const targetUser = username
      const level = -1
      const bankId = this.$route.params.bankId
      this.requestPermission({targetUser, level, bankId}).then(_ => {
        this.relistAccesses()
      }).catch(e => {
        console.log('could not remove access: ' + e)
      })
    },
  },
  created() {
    this.fetchImageList()
    this.relistAccesses()
  },
}
</script>
