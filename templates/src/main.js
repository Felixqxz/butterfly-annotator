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
import VueTippy, { TippyComponent } from 'vue-tippy'
import 'tippy.js/themes/google.css'

axios.defaults.withCredentials = true
const apiUrl = process.env.VUE_APP_ROOT_API
// default Flask port = 5000
axios.defaults.baseURL = apiUrl
Vue.prototype.$hostname = apiUrl

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VeeValidate, {
    inject: true,
    fieldsBagName: 'veeFields',
    errorBagName: 'veeErrors',
})
Vue.use(VueTippy, {
    directive: 'tippy',
})

Vue.component('tippy', TippyComponent)
Vue.config.productionTip = false
Vue.use(BootstrapVue)

new Vue({
    store,
    router,
    render: h => h(App),
}).$mount('#app')
