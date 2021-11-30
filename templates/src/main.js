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
// axios.defaults.baseURL = 'http://localhost:' + (process.env.PORT ? process.env.PORT : '5000')
// Vue.prototype.$hostname = 'http://localhost:' + (process.env.PORT ? process.env.PORT : '5000')
axios.defaults.baseURL = 'https://butterfly-annotator.herokuapp.com/:' + (process.env.PORT ? process.env.PORT : '5000')
Vue.prototype.$hostname = 'https://butterfly-annotator.herokuapp.com/:' + (process.env.PORT ? process.env.PORT : '5000')
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VeeValidate, {
    inject: true,
    fieldsBagName: 'veeFields',
    errorBagName: 'veeErrors',
})
Vue.use(VueTippy, {
    directive: 'tippy', // => v-tippy
})

Vue.component("tippy", TippyComponent);
Vue.config.productionTip = false
Vue.use(BootstrapVue)
// default Flask port = 5000

new Vue({
    store,
    router,
    render: h => h(App),
}).$mount('#app')
