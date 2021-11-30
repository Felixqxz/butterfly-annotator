import { createLocalVue, mount, shallowMount } from '@vue/test-utils'
import Header from '../../src/components/Header.vue'
import BootstrapVue, { BDropdownItem, BFormInput } from 'bootstrap-vue';
import Vuex from 'vuex'
import { render, fireEvent } from '@testing-library/vue'
import VueRouter from 'vue-router'
import router from "../../src/router/index.js"

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(BootstrapVue)
localVue.use(VueRouter)

describe('Header.vue', () => {
  let getters
  let store
  let actions

  actions = {
    logOut: jest.fn()
  }

  getters = {
    user: () => {
      return {
        username: 'zba',
        email: 'bz2818@ic.ac.uk'
      }
    },
    isLoggedIn: () => true
  }
  
  store = new Vuex.Store({
    // state: {
    //   todos: [
    //     { username: 'zba', email: 'bz2818@ic.ac.uk' },
    //   ]
    // },
    getters: {
      // currentUser: state => {
      //   return state.todos[0]
      // }
      currentUser: () => {
        return { username: 'zba', email: 'bz2818@ic.ac.uk' }
      },
      isLoggedIn: () => {
        return true
      }
    },
    actions
  })

  it('increments value on click', async () => {
    // The render method returns a collection of utilities to query your component.
    const {getByText} = render(Header, {
      localVue,
      store,
      router
    })

    const wrapper = shallowMount(Header, {
        localVue,
        store,
        router
      })

    const button = getByText('Profile')
    await fireEvent.click(button)
    console.log('route :', router.currentRoute)

    const button2 = getByText('Sign Out')
    await fireEvent.click(button2)
    console.log('new route :', router.currentRoute)
  })
})
