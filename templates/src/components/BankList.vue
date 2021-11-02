<template>
  <b-container>
    <b-row class="justify-content-center">
      <b-col cols="12">
        <h2 class="page-title">Your banks</h2>
      </b-col>
      <b-col cols="12">
        <div>
          <b-button v-b-modal.modal>Add a new bank</b-button>

          <b-modal id="modal" title="Create a new bank!">
            <b-form-input
              v-model="newBankName"
              placeholder="Enter the bank name"
              invalid-feedback="Name is required"
            ></b-form-input>
            <b-form-textarea
              id="textarea"
              v-model="newBankDiscription"
              placeholder="Enter a discription of the new bank"
              rows="3"
              max-rows="6"
            ></b-form-textarea>
            <template #modal-footer="{ cancel }">
              <b-button size="sm" variant="outline-secondary" @click="cancel()">
                Cancel
              </b-button>
              <b-button size="sm" variant="success" @click="createNewBank()">
                Create
              </b-button>
            </template>
          </b-modal>
        </div>
      </b-col>
    </b-row>
    <div class="bank-list">
      <b-row
        class="justify-content-center"
        v-for="bank in availableBanks"
        v-bind:key="bank.id"
      >
        <b-col cols="12">
          <router-link :to="'/bank/' + bank.name">
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
import { mapGetters, mapActions } from "vuex";
import axios from "axios";

export default {
  name: "BankList",
  computed: {
    ...mapGetters({ user: "currentUser", isLoggedIn: "isLoggedIn" }),
  },
  data() {
    return {
      availableBanks: [],
      newBankName: "",
      newBankDiscription: "",
    };
  },
  methods: {
    ...mapActions({ listBanks: "listBanks", addNewBank: "addNewBank" }),
    createNewBank() {
      if (this.newBankName === "") {
        return;
      }
      console.log(this.isLoggedIn ? this.user.username : "")
      let data = {
        bankName: this.newBankName,
        bankDiscription: this.newBankDiscription,
        userName: this.username(),
      };
      axios.post('http://localhost:5000' + '/api/bank/add', data)
          .then(res => {
            if (res.status !== 200) {
              console.log('Failed to add new bank, HTTP status=' + res.status) // TODO: handle correctly
            } else {
              console.log('success!')
              this.listAllBanks()
            }
          }).catch(err => {
            console.log(err) // TODO: handle errors properly
          })
      this.$bvModal.hide("modal");
    },
    username() {
      return this.isLoggedIn ? this.user.username : "";
    },
    listAllBanks() {
      let data = {
        userName: this.username(),
      }
      axios.post('http://localhost:5000' + '/api/bank/list', data)
          .then(res => {
            if (res.status !== 200) {
              console.log('Failed to add new bank, HTTP status=' + res.status) // TODO: handle correctly
            } else {
              this.availableBanks = res.data
            }
          }).catch(err => {
            console.log(err) // TODO: handle errors properly
          })
    },
  },
  created() {
    // this.listBanks()
    //   .then((req) => (this.availableBanks = req.data))
    //   .catch((err) => console.log(err)); // TODO: handle errors correctly
    this.listAllBanks()
  },
  
};
</script>
