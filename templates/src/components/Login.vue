<template>
  <div class="login_table">
    <b-card bg-variant="light">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          label-cols-lg="3"
          label="Please Sign In"
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

          <b-button type="submit" variant="primary">Sign in</b-button
          >&nbsp;&nbsp;
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form-group>
      </b-form>

      <br />

      <b-button variant="outline-primary" href="/register"
        >Need an account?</b-button
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