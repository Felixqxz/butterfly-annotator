<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info" class="mb-5">
      <b-navbar-brand href="/">Butterfly annotator</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="/">Home</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav>
          <b-nav-item href="/bank/1">Image Bank</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">

          <b-navbar-nav v-show="!hasLogin">
            <b-nav-item href="/register">Register</b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav v-show="!hasLogin">
            <b-nav-item href="/login">Login</b-nav-item>
          </b-navbar-nav>

          <b-nav-item-dropdown right v-show="hasLogin">

            <template #button-content>
              <em>{{username}}</em>
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item @click="logout()">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Header",
  data() {
    return {
      username: "user",
      hasLogin: false
    }
  },
  methods: {
    logout() {
      const _this = this
      axios.post(this.$hostname + "/logout").then(res => {
        _this.$store.commit("REMOVE_INFO")
        _this.$router.push("/login")
      })
    }
  },
  created() {
    if (this.$store.getters.getUser.username) {
      this.username = this.$store.getters.getUser.username
      this.hasLogin = true
    }
  }
}
</script>
