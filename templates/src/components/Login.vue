<template>
  <div>
    <Header></Header>
    <div id="login-row" class="row justify-content-center align-items-center">
      <div id="login-column" class="col-md-6">
        <div id="login-box" class="col-md-12">
          <b-form @submit="onSubmit" v-if="show">
            <h3 class="text-center text-info">Login</h3>
            <b-form-group class="form-group" id="input-group-1" label-for="username">
              <label class="text-info">Username:</label><br>
              <b-form-input class="form-control" id="username" v-model="form.username" required></b-form-input>
            </b-form-group>

            <b-form-group class="form-group" id="input-group-2" label-for="password">
              <label class="text-info">Password:</label><br>
              <b-form-input class="form-control" id="password" v-model="form.password" type="password"
                            required></b-form-input>
            </b-form-group>

            <b-button class="btn btn-info btn-md" type="submit" variant="primary">Sign in</b-button>

          </b-form>
          <br>
          <div class="text-left"><a href="/register" class="text-info">Need an account?</a></div>
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
      },
      show: true,
    };
  },
  methods: {
    onSubmit() {
      this.$refs[form].validate((valid) => {
        console.log("log...")
        if (valid) {
          const _this = this;
          axios.post(this.$hostname + "/login", this.form).then((res) => {
            console.log(res);
            const token = res.headers["authorization"];
            _this.$store.commit("SET_TOKEN", token);
            _this.$store.commit("SET_USERINFO", res.data.data);
            _this.$router.push("/");
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
  },
};
</script>
