import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import { render, fireEvent } from '@testing-library/vue'
import Login from '../../src/components/Login.vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import router from "../../src/router/index.js"
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)
Vue.config.silent = true

describe('Login.vue', () => {
  let actions
  let store
  let getters
  let wrapper

  beforeEach(() => {
    actions = {
      login: jest.fn(),
    }

    getters = {
      isLoggedIn: () => {
        return true
      }
    }

    store = new Vuex.Store({
      getters,
      actions
    })

    // wrapper = shallowMount(Login, { localVue, store })
  })

  it('test route redirecting after clicking "Sign in" button', async () => {
    const {getByText} = render(Login, {
      localVue,
      store,
      router,
      // data() {
      //   return {
      //     form: {
      //       username: '',
      //       password: '',
      //     },
      //   }
      // }
    })

    const signInButton = getByText('Sign in')
    const pathAfterClickSignInButton = '/settings'
    await fireEvent.click(signInButton)
    expect(actions.login).toHaveBeenCalled()

    expect(router.currentRoute.path).toMatch(pathAfterClickSignInButton)
  })

  it('test route redirecting after clicking "Need an account" button', async () => {
    const {getByText} = render(Login, {
      localVue,
      store,
      router
    })

    const registerButton = getByText('Need an account?')
    const pathAfterClickRegisterButton = '/register'
    await fireEvent.click(registerButton)

    expect(router.currentRoute.path).toMatch(pathAfterClickRegisterButton)
  })
})
