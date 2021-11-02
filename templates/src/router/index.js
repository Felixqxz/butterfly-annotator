import Vue from 'vue'
import Router from 'vue-router'
// import components
import AnnotateImage from '../components/AnnotateImage.vue'
import ImageList from '../components/ImageList.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import BankList from "../components/BankList.vue"

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'BankList',
      component: BankList,
    },
    {
      path: '/annotate/:bankName/:imageId',
      name: 'AnnotateImage',
      component: AnnotateImage,
    },
    {
      path: '/bank/:bankName',
      name: 'ImageList',
      component: ImageList
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { noAuth: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: { noAuth: true }
    },
  ],
})
