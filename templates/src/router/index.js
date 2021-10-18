import Vue from 'vue'
import Router from 'vue-router'
// import components
import Home from '../components/Home.vue'
import ImageList from '../components/ImageList.vue'
import BankList from "../components/BankList"

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/bank/:bankId',
      name: 'ImageList',
      component: ImageList
    },
    {
      path: '/bank-list',
      name: 'BankList',
      component: BankList
    }
  ],
})