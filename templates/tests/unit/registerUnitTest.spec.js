import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import { render, fireEvent } from '@testing-library/vue'
import Register from '../../src/components/Register.vue'
import Vuex from 'vuex'
import Vue from 'vue'
import VueRouter from 'vue-router'
import router from "../../src/router/index.js"

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)
Vue.config.silent = true

describe('Register.vue', () => {
  let actions
  let store
  let wrapper

  beforeEach(() => {
    actions = {
      registerAccount: jest.fn(),
    }

    store = new Vuex.Store({
      actions
    })

    // wrapper = shallowMount(Login, { localVue, store })
  })

  it('test route redirecting after clicking "Register" button', async () => {
    // const {getByText} = render(Register, {
    //   localVue,
    //   store,
    //   router
    // })

    // const registerButton = getByText('Register')
    // // console.log(registerButton)
    // const pathAfterClickRegisterButton = '/'
    // await fireEvent.click(registerButton)
    // expect(actions.registerAccount).toHaveBeenCalled()

    // expect(router.currentRoute.path).toMatch(pathAfterClickRegisterButton)
  })

  it('test route redirecting after clicking "Already have an account?" button', async () => {
    // const {getByText} = render(Register, {
    //   localVue,
    //   store,
    //   router
    // })

    // const loginButton = getByText('Already have an account?')
    // const pathAfterClickLoginButton = '/login'
    // await fireEvent.click(loginButton)

    // expect(router.currentRoute.path).toMatch(pathAfterClickLoginButton)
  })
})
