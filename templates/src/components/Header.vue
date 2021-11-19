<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark" class="mb-1">
      <b-navbar-brand>
        <router-link to="/">Butterfly annotator</router-link>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">

          <b-navbar-nav v-show="!isLoggedIn">
            <b-nav-item>
              <router-link to="/register">Register</router-link>
            </b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav v-show="!isLoggedIn">
            <b-nav-item>
              <router-link to="/login">Login</router-link>
            </b-nav-item>
          </b-navbar-nav>

          <b-nav-item-dropdown right v-show="isLoggedIn">

            <template #button-content>
              <em>{{ username() }}</em>
            </template>
            <!-- <router-link to="/profile"> -->
              <b-dropdown-item @click="goProfile()">Profile</b-dropdown-item>
            <!-- </router-link> -->
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
  color: #fff;
  transition: color 0.2s;
}

.navbar-brand a:hover {
  color: rgb(211, 211, 211) !important;
}

.nav-item a {
  transition: color 0.2s;
}

.nav-item a:hover {
  color: rgb(172, 172, 172) !important;
}

.dropdown-menu li {
  color: red !important;
}

</style>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Header',
  computed: {
    ...mapGetters({ user: 'currentUser', isLoggedIn: 'isLoggedIn' }),
  },
  methods: {
    ...mapActions({ doLogOut: 'logOut' }),
    logout() {
      const t = this
      this.doLogOut().then(_ => t.$router.push('/login'))
    },
    username() {
      return this.isLoggedIn ? this.user.username : ''
    },
    goProfile() {
      this.$router.push('/profile')
    }
  },
}
</script>
