<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-12">
        <h2 class="page-title">Your banks</h2>
      </div>
    </div>
    <div class="bank-list">
      <div class="row justify-content-center" v-for="bank in availableBanks" v-bind:key="bank.id">
        <div class="col-12">
          <router-link :to="'/bank/' + bank.id">
            <div class="card card-hover bank-list-card">
              <div class="card-body">
                <h5 class="card-title">
                  {{ bank.name }}
                </h5>
                <p class="card-text text-muted">
                  {{ bank.description }}
                </p>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      availableBanks: [],
    }
  },
  created() {
    axios.get(this.$hostname + '/api/bank-list')
        .then(req => this.availableBanks = req.data)
        .catch(err => console.log(err)) // TODO: handle errors correctly
  },
}
</script>
