import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import * as VeeValidate from 'vee-validate'
import * as _ from './permission'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:' + (process.env.PORT ? process.env.PORT : '5000')
Vue.use(VeeValidate, {
    inject: true,
    fieldsBagName: 'veeFields',
    errorBagName: 'veeErrors',
})
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
// Vue.loadScript("sketch.js")
// default Flask port = 5000

new Vue({
    store,
    router,
    render: h => h(App),
}).$mount('#app')
