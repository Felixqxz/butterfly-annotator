<template>
  <div class="login_table">
    <b-card bg-variant="light">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          label-cols-lg="3"
          label="Please Register"
          label-align-lg="center"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-0"
        >
          <br />
          <b-form-group
            label-cols-sm="3"
            label-align-sm="center"
            id="input-group-1"
            label="Username:"
            label-for="input-1"
          >
            <b-form-input
              id="input-1"
              v-model="form.username"
              required
              placeholder="Enter username"
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label-cols-sm="3"
            label-align-sm="center"
            id="input-group-2"
            label="Password:"
            label-for="input-2"
          >
            <b-form-input
              id="input-2"
              v-model="form.password"
              type="password"
              required
              placeholder="Enter password"
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label-cols-sm="3"
            label-align-sm="center"
            id="input-group-3"
            label="Confirm password:"
            label-for="input-3"
          >
            <b-form-input
              id="input-3"
              v-model="form.confirmedPassword"
              type="password"
              required
              placeholder="Enter password again"
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label-cols-sm="3"
            label-align-sm="center"
            id="input-group-4"
            label="Email:"
            label-for="input-4"
          >
            <b-form-input
              id="input-4"
              v-model="form.email"
              type="email"
              required
              placeholder="Enter email"
            ></b-form-input>
          </b-form-group>

          <b-button type="submit" variant="primary">Register</b-button>&nbsp;&nbsp;
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form-group>
      </b-form>

      <br />

      <b-button variant="outline-primary" href="/login"
        >Already have an account?</b-button
      >
    </b-card>
  </div>
</template>

<script>
export default {
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
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.username = "";
      this.form.password = "";
      this.form.confirmedPassword = "";
      this.form.email = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style>
.login_table {
  margin: 50px 100px;
  text-align: center;
}
</style>