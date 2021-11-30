import { createLocalVue } from '@vue/test-utils'
import { render, fireEvent } from '@testing-library/vue'
import Header from '../../src/components/Header.vue'
import Vuex from 'vuex'
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

  it('test route redirecting after clicking "Profile" button', async () => {
    // The render method returns a collection of utilities to query your component.
    const {getByText} = render(Header, {
      localVue,
      store,
      router
    })
    const profileButton = getByText('Profile')
    const pathAfterClickProfileButton = '/settings'
    await fireEvent.click(profileButton)

    expect(router.currentRoute.path).toMatch(pathAfterClickProfileButton)
  })

  it('test route redirecting after clicking "Sign out" button', async () => {
    const {getByText} = render(Header, {
      localVue,
      store,
      router
    })

    const signOutButton = getByText('Sign Out')
    const pathAfterClickSignOutButton = '/login'
    await fireEvent.click(signOutButton)

    // This test also need to test whether the 'logout' function is called after clicking the button
    expect(actions.logOut).toHaveBeenCalled()
    
    expect(router.currentRoute.path).toMatch(pathAfterClickSignOutButton)
  })

  it('test route redirecting after clicking "Butterfly annotator" button', async () => {
    const {getByText} = render(Header, {
      localVue,
      store,
      router
    })

    const butterflyAnnotatorButton = getByText('Butterfly annotator')
    const pathAfterClickButterflyAnnotatorButton = '/'
    await fireEvent.click(butterflyAnnotatorButton)

    expect(router.currentRoute.path).toMatch(pathAfterClickButterflyAnnotatorButton)
  })

  it('test route redirecting after clicking "Register" button', async () => {
    const {getByText} = render(Header, {
      localVue,
      store,
      router
    })

    const registerButton = getByText('Register')
    const pathAfterClickRegisterButton = '/register'
    await fireEvent.click(registerButton)

    expect(router.currentRoute.path).toMatch(pathAfterClickRegisterButton)
  })

  it('test route redirecting after clicking "Login" button', async () => {
    const {getByText} = render(Header, {
      localVue,
      store,
      router
    })

    const loginButton = getByText('Login')
    const pathAfterClickLoginButton = '/login'
    await fireEvent.click(loginButton)

    expect(router.currentRoute.path).toMatch(pathAfterClickLoginButton)
  })
})
