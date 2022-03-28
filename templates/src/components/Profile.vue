<template>
  <b-container>
    <b-row>
      <b-col cols="12">
        <h2>User profile</h2>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="8" xs="12">
        <b-form>
          <label for="username-input">Username</label>
          <b-form-input type="text" id="username-input"
                        disabled :value="username" class="mb-2"/>
          <label for="email-input">Email</label>
          <b-form-input type="text" id="email-input" disabled :value="email"/>
        </b-form>
      </b-col>
      <b-col md="4" xs="12">
        <profile-picture :picture="$hostname + '/api/profile-picture/' + username" :editable="false" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ProfilePicture from './ProfilePicture'
import {mapActions} from 'vuex'
import handleError from '../errors/handler'

export default {
  name: 'Profile',
  data() {
    return {
      username: '',
      email: '',
    }
  },
  components: {
    ProfilePicture,
  },
  methods: {
    ...mapActions({fetchUserData: 'fetchUserData'}),
  },
  created() {
    this.fetchUserData({username: this.$route.params.username}).then(res => {
      this.username = res.data.username
      this.email = res.data.email
    }).catch(e => handleError(this.$bvToast, 'Could not load user info', `Cause: ${e.response.data.message}`))
  },
}
</script>
