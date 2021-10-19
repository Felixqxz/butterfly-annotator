import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import { BootstrapVue } from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)

Vue.config.productionTip = false
Vue.prototype.$hostname = 'http://localhost:' + (process.env.PORT ? process.env.PORT : '5000')
Vue.use(BootstrapVue)
// default Flask port = 5000

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
