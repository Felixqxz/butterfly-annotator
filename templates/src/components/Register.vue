<template>
  <div>
    <div id="login-row" class="row justify-content-center align-items-center">
      <div id="login-column" class="col-md-6">
        <div id="login-box" class="col-md-12">
          <b-form :model="registrationForm" ref="registrationForm" autocomplete="off">
            <h3 class="text-center ">Register</h3>
            <b-form-group
                class="form-group"
                id="input-group-1"
                label-for="username">
              <label class="">Username:</label><br/>
              <b-form-input
                  class="form-control"
                  id="username"
                  name="username"
                  v-model="registrationForm.username"
                  v-validate="{ required: true }"
                  :state="validateState('username')"></b-form-input>
              <b-form-invalid-feedback id="username">{{
                  veeErrors.first('username')
                }}
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group
                id="input-group-2"
                label-for="password">
              <label class="">Password:</label><br/>
              <b-form-input
                  id="password"
                  name="password"
                  ref="password"
                  v-model="registrationForm.password"
                  type="password"
                  v-validate="{ required: true }"
                  :state="validateState('password')"
              ></b-form-input>
              <b-form-invalid-feedback id="password">{{
                  veeErrors.first('password')
                }}
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group
                id="input-group-3"
                label-for="confirmedPassword">
              <label class="">Confirm your password:</label><br/>
              <b-form-input
                  id="confirmedPassword"
                  name="confirmedPassword"
                  v-model="registrationForm.confirmedPassword"
                  type="password"
                  v-validate="'required|confirmed:password'"
                  :state="validateState('confirmedPassword')"></b-form-input>
              <b-form-invalid-feedback id="confirmedPassword">{{
                  veeErrors.first('confirmedPassword')
                }}
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group id="input-group-4" label-for="email">
              <label>Email:</label><br/>
              <b-form-input
                  id="email"
                  name="email"
                  v-model="registrationForm.email"
                  type="email"
                  v-validate="{ required: true, email: true }"
                  :state="validateState('email')"></b-form-input>
              <b-form-invalid-feedback id="email">{{
                  veeErrors.first('email')
                }}
              </b-form-invalid-feedback>
            </b-form-group>

            <b-button
                class="btn-md"
                variant="dark"
                @click="submitForm()"
                type="primary">Register
            </b-button>&nbsp;&nbsp;
          </b-form>
          <br/>
          <div class="text-left">
            <router-link to="/login" class="">Already have an account?</router-link>
          </div>
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
      registrationForm: {
        username: '',
        password: '',
        confirmedPassword: '',
        email: '',
      },
    }
  },
  methods: {
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
      this.$validator.validateAll().then((valid) => {
        if (valid) {
          axios.post(this.$hostname + '/register', this.registrationForm).then(res => {
            const token = res.data.data.username
            t.$store.commit('SET_TOKEN', token)
            t.$store.commit('SET_USERINFO', res.data.data)
            // _this.$router.push("/");
          })
          t.$router.push('/')
        } else {
          // TODO: handle errors correctly
        }
      })
    },
  },
}
</script>