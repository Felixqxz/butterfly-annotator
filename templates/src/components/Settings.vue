<template>
  <b-container>
    <b-row>
      <b-col cols="12">
        <h2>Your profile</h2>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="8" xs="12">
        <b-form>
          <label for="username-input">Username</label>
          <b-form-input type="text" id="username-input"
                        disabled :value="currentUser.username" class="mb-2"/>
          <label for="email-input">Email</label>
          <b-form-input type="text" id="email-input" disabled :value="currentUser.email"/>
        </b-form>
      </b-col>
      <b-col md="4" xs="12">
        <profile-picture :picture="$hostname + '/api/profile-picture/' + currentUser.username" :editable="true" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ProfilePicture from "./ProfilePicture"

import {mapGetters} from 'vuex'

export default {
  name: 'Settings',
  components: {
    ProfilePicture,
  },
  computed: {
    ...mapGetters({currentUser: 'currentUser'}),
  },
  data() {
    return {
      profilePicture: null,
      imagePlaceholder: { blank: true, blankColor: '#777', width: 75, height: 75, class: 'm1' },
    }
  },
}
</script>

<style>
.form-control:disabled {
  background-color: transparent;
  cursor: text;
  border-color: transparent;
  box-shadow: none;
  outline-color: transparent;
}
</style>
