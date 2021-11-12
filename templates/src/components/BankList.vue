<template>
  <b-container>
    <b-row class="mb-2">
      <b-col md="2" xs="12" class="justify-content-center">
        <label for="id_avator">
          <b-avatar id="avator" :src="imgSrc(avatarPath)" size="72px"></b-avatar>
        </label>
        <div v-show="false">
          <b-form-file
            id="id_avator"
            v-model="avatarName"
            accept="image/*"
          ></b-form-file>
        </div>
        <b-form-textarea
          id="textarea"
          v-model="text"
          placeholder="Enter something..."
          rows="9"
          @change="edit"
        ></b-form-textarea>
        <b-button @click="save()" :disabled="edited">
          Save
        </b-button>
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
import axios from "axios";
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'BankList',
  data() {
    return {
      availableBanks: [],
      avatarPath: '',
      userName: "",
      avatarName: null,
      edited: true,
      text: '',
    }
  },
  watch: {
    avatarName(val, oldVal) {
      this.edited = false
    }
  },
  computed: {
    ...mapGetters({ user: 'currentUser', isLoggedIn: 'isLoggedIn' }),
  },
  methods: {
    ...mapActions({listBanks: 'listBanks', getAvatar: 'getAvatar'}),
    updateBanks() {
      this.listBanks().then(req => this.availableBanks = req.data)
          .catch(err => console.log(err)) // TODO: handle errors correctly
    },
    getAvatarPath() {
      this.userName = this.isLoggedIn ? this.user.username : ''
      this.getAvatar()
        .then(res => {
          if (res.status === 200) {
            console.log(res)
            this.avatarPath = res.data.avatar == "null" ? "" : res.data.avatar
            console.log("text", this.text)
            let discription = res.data.discription == "null" ? "" : res.data.discription
            if (this.text != discription) {
              this.text = discription
            }
          } else {
            console.log("F!")
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    edit() {
      this.edited = false
    },
    imgSrc(imageUrl) {
      if (imageUrl === undefined || imageUrl === null || imageUrl === "") {
        return
      }
      // In this case, the imageUrl is from fileReader.readAsDataURL which means we don't need to parse it
      if (imageUrl.indexOf(",") > 0) {
        return imageUrl
      }
      return require("../../../website/static/avatar/" + imageUrl);
    },
    save() {
      // if (this.avatarName == null) {
      //   return
      // }

      let formData = new FormData();
      console.log(this.text)

      if (this.avatarName == null) {
        var file = new File([""], "avatarFile")
        formData.append("avatarFile", file)
        formData.append('avatarName', null)
      } else {
        formData.append("avatarFile", this.avatarName)
        formData.append('avatarName', this.avatarName.name)
      }

      formData.append('username', this.userName)
      formData.append('discription', this.text)

      axios
        .post(this.$hostname + "/api/avatar/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log("res", res)
          if (res.status == 200) {
            console.log("success!")
            this.getAvatarPath()
            this.edited = true
          } else {
            console.log("fail!")
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    preview() {
      let t = this
      document.getElementById('id_avator').onchange = function () {
        var imgFile = this.files[0]
        var fr = new FileReader()
        fr.onload = function () {
          t.avatarPath = fr.result
        }
        fr.readAsDataURL(imgFile)
      }
    },
  },
  mounted() {
    this.preview()
  },
  created() {
    this.updateBanks()
    this.getAvatarPath()
  },
}
</script>
<style scoped>
.bank-list-card {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
