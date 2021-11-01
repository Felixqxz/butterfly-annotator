<template>
  <b-container>
    <b-row class="justify-content-center">
      <b-col cols="12">
        <h2 class="page-title">Your banks</h2>
      </b-col>
      <b-col cols="12">
        <b-button type="button">
          Add
        </b-button>
      </b-col>
    </b-row>
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
  </b-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'BankList',
  computed: {
    ...mapGetters({ user: 'currentUser', isLoggedIn: 'isLoggedIn' }),
  },
  data() {
    return {
      availableBanks: [],
    }
  },
  methods: {
    ...mapActions({ listBanks: 'listBanks' })
  },
  created() {
    this.listBanks().then(req => this.availableBanks = req.data)
        .catch(err => console.log(err)) // TODO: handle errors correctly
  },
  username() {
      return this.isLoggedIn ? this.user.username : ''
  },
}
</script>
