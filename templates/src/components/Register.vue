<template>
  <div>
    <Header></Header>
    <div id="login-row" class="row justify-content-center align-items-center">
      <div id="login-column" class="col-md-6">
        <div id="login-box" class="col-md-12">
          <b-form :model="registrationForm" ref="registrationForm">
            <h3 class="text-center text-info">Register</h3>
            <b-form-group class="form-group" id="input-group-1" label-for="username">
              <label class="text-info">Username:</label><br>
              <b-form-input class="form-control" id="username" v-model="registrationForm.username" required></b-form-input>
            </b-form-group>

            <b-form-group class="form-group" id="input-group-2" label-for="password">
              <label class="text-info">Password:</label><br>
              <b-form-input class="form-control" id="password" v-model="registrationForm.password" type="password"
                            required></b-form-input>
            </b-form-group>

            <b-form-group class="form-group" id="input-group-3" label-for="confirm_password">
              <label class="text-info">Confirm your password:</label><br>
              <b-form-input id="confirm_password" v-model="registrationForm.confirmedPassword" type="password" required
              ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-4" label-for="email">
              <label class="text-info">Email:</label><br>
              <b-form-input id="email" v-model="registrationForm.email" type="email" required
              ></b-form-input>
            </b-form-group>

            <b-button class="btn btn-info btn-md" type="submit" @click="submitForm('registrationForm')" variant="primary">Register</b-button>&nbsp;&nbsp;

          </b-form>
          <br>
          <div class="text-left"><a href="/login" class="text-info">Already have an account?</a></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/Header.vue'
import axios from 'axios'

export default {
  components: {
    Header
  },
  data() {
    return {
      registrationForm: {
        username: "",
        password: "",
        confirmedPassword: "",
        email: ""
      },
      submitted: false
    };
  },
  methods: {
    submitForm(formName) {
      console.log("hhh")
      console.log("register...")
      //
      axios.post(this.$hostname + "/register", this.registrationForm).then((res) => {
        console.log(res)
      })

      //     // const token = res.headers["authorization"];
      //     // this.$store.commit("SET_TOKEN", token);
      //     // this.$store.commit("SET_USERINFO", res.data.data);
      // this.$router.push("/");


      console.log('hi')
    },
  }
};
</script>