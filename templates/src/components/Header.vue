<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark" class="mb-5">
      <b-navbar-brand>
        <router-link to="/">Butterfly annotator</router-link>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item>
            <router-link to="/bank-list">Image Bank</router-link>
          </b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">

          <b-navbar-nav v-show="!hasLogin">
            <b-nav-item>
              <router-link to="/register">Register</router-link>
            </b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav v-show="!hasLogin">
            <b-nav-item>
              <router-link :to="'/login'">Login</router-link>
            </b-nav-item>
          </b-navbar-nav>

          <b-nav-item-dropdown right v-show="hasLogin">

            <template #button-content>
              <em>{{ username }}</em>
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item @click="logout()">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<style>
nav li:hover,
nav li.router-link-active,
nav li.router-link-exact-active {
  cursor: pointer;
}

nav li a, .navbar-brand a {
  text-decoration: none !important;
  color: white !important;
  transition: color 0.2s;
}

nav li a:hover, .navbar-brand a:hover {
  color: lightgray !important;
}

</style>

<script>
import axios from 'axios'

export default {
  name: 'Header',
  data() {
    return {
      username: 'user',
      hasLogin: false,
    }
  },
  methods: {
    logout() {
      const t = this
      axios.post(this.$hostname + '/logout').then(_ => {
        t.$store.commit('REMOVE_INFO')
        t.$router.push('/login')
      })
    },
  },
  created() {
    if (this.$store.getters.getUser.username) {
      this.username = this.$store.getters.getUser.username
      this.hasLogin = true
    }
  },
}
</script>
