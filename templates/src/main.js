import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import { BootstrapVue } from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import * as VeeValidate from 'vee-validate';

Vue.use(BootstrapVue)
Vue.use(VeeValidate, {
  inject: true,
  fieldsBagName: "veeFields",
  errorBagName: "veeErrors"
});
Vue.config.productionTip = false
Vue.prototype.$hostname = 'http://localhost:' + (process.env.PORT ? process.env.PORT : '5000')
Vue.use(BootstrapVue)
// default Flask port = 5000

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
