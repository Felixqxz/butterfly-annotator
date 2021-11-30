import { createLocalVue, mount } from '@vue/test-utils'
import Header from '../../src/components/Header.vue'
import Vuex from 'vuex'
import { render, fireEvent } from '@testing-library/vue'
import VueRouter from 'vue-router'
import router from "../../src/router/index.js"

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

describe('Header.vue', () => {
  let getters
  let store
  let actions

  actions = {
    logOut: jest.fn()
  }

  getters = {
    currentUser: () => {
      return { username: 'zba', email: 'bz2818@ic.ac.uk' }
    },
    isLoggedIn: () => {
      return true
    }
  }
  
  store = new Vuex.Store({
    getters,
    actions
  })

  it('increments value on click', async () => {
    // The render method returns a collection of utilities to query your component.
    const {getByText} = render(Header, {
      localVue,
      store,
      router
    })

    const wrapper = mount(Header, {
        localVue,
        store,
        router
      })

    const profileButton = getByText('Profile')
    const pathAfterClickProfileButton = '/settings'
    await fireEvent.click(profileButton)
    // console.log('route :', router.currentRoute.path)
    expect(router.currentRoute.path).toMatch(pathAfterClickProfileButton)

    const signOutButton = getByText('Sign Out')
    const pathAfterClickSignOutButton = '/login'
    await fireEvent.click(signOutButton)
    expect(actions.logOut).toHaveBeenCalled()
    // console.log('new route :', router.currentRoute.path)
    expect(router.currentRoute.path).toMatch(pathAfterClickSignOutButton)
  })
})
