<template>
  <b-container>
    <!-- <b-row class="justify-content-center">
      <b-col cols="12">
        
      </b-col>
    </b-row> -->
    <b-row class="mb-2">
      <b-col md="2" xs="12" class="justify-content-center">
        <!-- <b-avatar src="https://placekitten.com/300/300" size="72px"></b-avatar> -->
        <label for="id_avator">
          <b-avatar :src="imgSrc(avatarPath)" size="72px" @click="overrideName"></b-avatar>
        </label>
        <!-- <div v-show="seen"> -->
          <b-form-file
            id="id_avator"
            v-model="avatarName"
            accept=".jpg, .png, .gif, .jpeg"
            @click="overrideName"
          ></b-form-file>
        <!-- </div> -->
      </b-col>
      <b-col md="10" xs="12">
        <h2 class="page-title">Your banks</h2>
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
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'BankList',
  data() {
    return {
      availableBanks: [],
      avatarPath: '',
      userName: "",
      seen: false,
      avatarName: null,
    }
  },
  computed: {
    ...mapGetters({ user: 'currentUser', isLoggedIn: 'isLoggedIn' }),
  },
  methods: {
    ...mapActions({listBanks: 'listBanks'}),
    updateBanks() {
      this.listBanks().then(req => this.availableBanks = req.data)
          .catch(err => console.log(err)) // TODO: handle errors correctly
    },
    getAvatarPath() {
      this.avatarPath = this.isLoggedIn ? this.user.avatar : ''
    },
    imgSrc(imageName) {
      return require("../../../website/static/avatar/" + imageName);
    },
    save() {
      
      axios.post(this.$hostname + '/api/', {
        image_id: imageId
      }) 
    },
    overrideName() {
      console.log(this.avatarName)
    }
    // user() {
    //   this.userName = this.isLoggedIn ? this.user : ''
    // },
  },
  created() {
    this.updateBanks()
    this.getAvatarPath()
    // this.username()
  },
}
</script>
<style scoped>
.bank-list-card {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>