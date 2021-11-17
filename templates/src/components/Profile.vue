<template>
  <b-container>
    <b-row class="mb-2">
      <b-col md="2" xs="12" class="justify-content-center">
        <b-row align-h="center">
          <label for="id_avator">
            <b-avatar id="avator" :src="imgSrc(avatarName)" size="6rem" 
            rounded="circle" badge-variant="dark">
              <!-- <template #badge><b-icon icon="camera" font-scale="1"></b-icon></template> -->
            </b-avatar>
          </label>
        </b-row>
        <div v-show="false">
          <b-form-file
            id="id_avator"
            v-model="avatarFile"
            accept="image/*"
          ></b-form-file>
        </div>
        <b-form-textarea
          id="textarea"
          v-model="text"
          placeholder="Enter something..."
          rows="15"
          max-rows="100"
          @change="edit"
        ></b-form-textarea>

        <b-row align-h="center">
          <b-button variant="outline-primary" size="sm" @click="save()" :disabled="edited">
            Save
          </b-button>
        </b-row>
      </b-col>

      <b-col md="10" xs="12">
      <h2 class="page-title">Account Settings</h2>
        
        <br><br>
        <b-row class="my-1">
          <b-col sm="3">
            <code class="label-text-font">FirstName</code>:
          </b-col>
          <b-col sm="6">
            <b-form-input size="lg" v-model="firstName" @change="update"></b-form-input>
          </b-col>
        </b-row>
        <br>

        <b-row class="my-1">
          <b-col sm="3">
            <code class="label-text-font">LastName</code>:
          </b-col>
          <b-col sm="6">
            <b-form-input size="lg" v-model="lastName" @change="update"></b-form-input>
          </b-col>
        </b-row>
        <br>

        <b-row class="my-1">
          <b-col sm="3">
            <code class="label-text-font">Email</code>:
          </b-col>
          <b-col sm="6">
            <b-form-input size="lg" v-model="email"></b-form-input>
          </b-col>
        </b-row>
        <br>

        <b-row class="my-1">
          <b-col sm="3">
            <code class="label-text-font">Username</code>:
          </b-col>
          <b-col sm="6">
            <b-form-input size="lg" v-model="userName"></b-form-input>
          </b-col>
        </b-row>

        <b-row align-h="center">
          <b-button variant="outline-primary" size="sm" @click="updateInfo()" :disabled="updated">
            Update
          </b-button>
        </b-row>

      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import { mapGetters, mapActions } from 'vuex'
import { BIcon } from 'bootstrap-vue'

export default {
  components: {
    BIcon,
  },
  name: 'Profile',
  data() {
    return {
      avatarName: '',
      userName: "",
      avatarFile: null,
      edited: true,
      updated: true,
      text: '',
      firstName: '',
      lastName: '',
      email: '',
    }
  },
  watch: {
    avatarFile(val, oldVal) {
      this.edited = false
    }
  },
  computed: {
    ...mapGetters({ user: 'currentUser', isLoggedIn: 'isLoggedIn' }),
  },
  methods: {
    ...mapActions({ getAvatar: 'getAvatar', getUserInfo: 'getUserInfo' }),
    getAvatarPath() {
      this.userName = this.isLoggedIn ? this.user.username : ''
      this.getAvatar()
        .then(res => {
          if (res.status === 200) {
            this.avatarName = res.data.avatar == "null" ? "" : res.data.avatar
            let description = res.data.description == "null" ? "" : res.data.description
            if (this.text != description) {
              this.text = description
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
    update() {
      this.updated = false
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
      let formData = new FormData()
      console.log(this.text)

      if (this.avatarFile == null) {
        var file = new File([""], "avatarFile")
        formData.append("avatarFile", file)
        formData.append('avatarName', null)
      } else {
        formData.append("avatarFile", this.avatarFile)
        formData.append('avatarName', this.avatarFile.name)
      }

      formData.append('username', this.userName)
      formData.append('description', this.text)

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
    updateInfo() {
      let formData = new FormData()
      formData.append('firstName', this.firstName)
      formData.append('lastName', this.lastName)

      axios
        .post(this.$hostname + "/api/info/update", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log("res", res)
          if (res.status == 200) {
            console.log("success!")
            this.getInfo()
            this.updated = true
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
          t.avatarName = fr.result
        }
        fr.readAsDataURL(imgFile)
      }
    },
    getInfo() {
      this.getUserInfo()
        .then((res) => {
          console.log("res", res)
          if (res.status == 200) {
            let data = res.data
            this.firstName = data.firstName
            this.lastName = data.lastName
            this.email = data.email
          } else {
            console.log("fail!")
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.preview()
  },
  created() {
    this.getAvatarPath()
    this.getInfo()
  },
}
</script>
<style scoped>
.bank-list-card {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
.label-text-font {
  font-size: 25px;
}
</style>
