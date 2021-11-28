<template>
  <b-container>
    <b-row class="justify-content-center">
      <b-col cols="12">
        <h2 class="page-title">Your banks</h2>
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
import {mapActions} from 'vuex'
import handleError from '../errors/handler'

export default {
  name: 'BankList',
  data() {
    return {
      availableBanks: [],
    }
  },
  methods: {
    ...mapActions({listBanks: 'listBanks'}),
    updateBanks() {
      this.listBanks().then(req => this.availableBanks = req.data)
          .catch(err => handleError(this.$bvToast, 'Cannot list banks',
              `Cause: ${err.response.data.message}`))
    }
  },
  created() {
    this.updateBanks()
  },
}
</script>
<style scoped>
.bank-list-card {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
