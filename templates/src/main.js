import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'

Vue.config.productionTip = false
Vue.prototype.$hostname = 'http://localhost:5000'

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app')
