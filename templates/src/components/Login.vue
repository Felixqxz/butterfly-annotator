<template>
  <div>
    <Header></Header>
    <div id="login-row" class="row justify-content-center align-items-center">
      <div id="login-column" class="col-md-6">
        <div id="login-box" class="col-md-12">
          <b-form>
            <h3 class="text-center text-info">Login</h3>
            <b-form-group
              class="form-group"
              id="input-group-1"
              label-for="username"
            >
              <label class="text-info">Username:</label><br />
              <b-form-input
                class="form-control"
                id="username"
                name="username"
                v-model="form.username"
                v-validate="'required'"
                :state="validateState('username')"
              ></b-form-input>
              <b-form-invalid-feedback id="username">{{
                veeErrors.first("username")
              }}</b-form-invalid-feedback>
            </b-form-group>

            <b-form-group
              class="form-group"
              id="input-group-2"
              label-for="password"
            >
              <label class="text-info">Password:</label><br />
              <b-form-input
                class="form-control"
                id="password"
                name="password"
                v-model="form.password"
                type="password"
                v-validate="'required'"
                :state="validateState('password')"
              ></b-form-input>
              <b-form-invalid-feedback id="password">{{
                veeErrors.first("password")
              }}</b-form-invalid-feedback>
            </b-form-group>

            <b-button
              class="btn btn-info btn-md"
              type="submit"
              @click="submitForm()"
              variant="primary"
              >Sign in</b-button
            >
          </b-form>
          <br />
          <div class="text-left">
            <a href="/register" class="text-info">Need an account?</a>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import axios from "axios";

export default {
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    validateState(ref) {
      if (
        this.veeFields[ref] &&
        (this.veeFields[ref].dirty || this.veeFields[ref].validated)
      ) {
        return !this.veeErrors.has(ref);
      }
      return null;
    },
    submitForm() {
      const _this = this;
      this.$validator.validateAll().then((valid) => {
        if (valid) {
          axios.post(this.$hostname + "/login", this.form).then((res) => {
            if (res.data.status == '200') {
              console.log(res.data)
              const token = res.data.data.username;
            // console.log(token)
              _this.$store.commit("SET_TOKEN", token);
              _this.$store.commit("SET_USERINFO", res.data.data);
              // this.$router.push("/");
            } else {
              console.log(res.data.data.message)
              return;
            }
          });
          this.$router.push("/");
        } else {
          console.log("error submit")
          return;
        }
      });
    },
  },
};
</script>
