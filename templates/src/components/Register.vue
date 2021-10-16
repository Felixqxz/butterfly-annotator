<template>
  <div class="container">
    <Header></Header>
    <div id="login-row" class="row justify-content-center align-items-center">
      <div id="login-column" class="col-md-6">
        <div id="login-box" class="col-md-12">
          <b-form @submit="onSubmit" v-if="show">
            <h3 class="text-center text-info">Register</h3>
            <b-form-group class="form-group" id="input-group-1" label-for="username">
              <label class="text-info">Username:</label><br>
              <b-form-input class="form-control" id="username" v-model="form.username" required></b-form-input>
            </b-form-group>

            <b-form-group class="form-group" id="input-group-2" label-for="password">
              <label class="text-info">Password:</label><br>
              <b-form-input class="form-control" id="password" v-model="form.password" type="password"
                            required></b-form-input>
            </b-form-group>

            <b-form-group class="form-group" id="input-group-3" label-for="confirm_password">
              <label class="text-info">Confirm your password:</label><br>
              <b-form-input id="confirm_password" v-model="form.confirmedPassword" type="password" required
              ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-4" label-for="email">
              <label class="text-info">Email:</label><br>
              <b-form-input id="email" v-model="form.email" type="email" required
              ></b-form-input>
            </b-form-group>

            <b-button class="btn btn-info btn-md" type="submit" variant="primary">Register</b-button>&nbsp;&nbsp;

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

export default {
  components: {
    Header
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
        confirmedPassword: "",
        email: ""
      },
      show: true,
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    },
  },
};
</script>