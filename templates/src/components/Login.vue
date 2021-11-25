<template>
  <div>
    <div id="login-row" class="row justify-content-center align-items-center">
      <div id="login-column" class="col-md-6">
        <div id="login-box" class="col-md-12">
          <b-form autocomplete="off">
            <h3 class="text-center">Login</h3>
            <b-form-group
                id="input-group-1"
                label-for="username">
              <label>Username:</label>
              <b-form-input
                  id="username"
                  name="username"
                  v-model="form.username"
                  v-validate="'required'"
                  :state="validateState('username')"
                  v-on:keyup.enter="submitForm()"
              ></b-form-input>
              <b-form-invalid-feedback id="username">{{ veeErrors.first('username') }}</b-form-invalid-feedback>
            </b-form-group>

            <b-form-group
                id="input-group-2"
                label-for="password">
              <label>Password:</label>
              <b-form-input
                  id="password"
                  name="password"
                  v-model="form.password"
                  type="password"
                  v-validate="'required'"
                  :state="validateState('password')"
                  v-on:keyup.enter="submitForm()"
              ></b-form-input>
              <b-form-invalid-feedback id="password">{{
                  veeErrors.first('password')
                }}
              </b-form-invalid-feedback>
            </b-form-group>

            <b-button
                class="btn-md"
                variant="dark"
                @click="submitForm()">Sign in
            </b-button>
          </b-form>
          <div class="text-left" style="margin-top: 1em;">
            <router-link to="/register">Need an account?</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import handleError from '../errors/handler'

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    }
  },
  computed: {
    ...mapGetters({isLoggedIn: 'isLoggedIn'}),
  },
  methods: {
    ...mapActions({ logIn: 'logIn' }),
    validateState(ref) {
      if (
          this.veeFields[ref] &&
          (this.veeFields[ref].dirty || this.veeFields[ref].validated)
      ) {
        return !this.veeErrors.has(ref)
      }
      return null
    },
    submitForm() {
      const t = this
      const formData = this.form
      this.$validator.validateAll().then(valid => {
        if (valid) {
          this.logIn({formData}).then(_ => {
            t.$router.push({ path: '/' })
          }).catch(e => {
            handleError(this.$bvToast, 'Error: could not login', `Cause: ${e.response.data.message}`)
          })
        }
      })
    },
  },
  created() {
    if (this.isLoggedIn) {
      this.$router.push({path: '/'})
    }
  },
}
</script>
