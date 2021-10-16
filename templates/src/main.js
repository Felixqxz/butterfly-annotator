import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'

Vue.config.productionTip = false
// default Flask port = 5000
Vue.prototype.$hostname = 'http://localhost:' + (process.env.PORT ? process.env.PORT : '5000')

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
