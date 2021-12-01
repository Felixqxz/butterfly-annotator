import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import ImageList from '../../src/components/ImageList.vue'
import Vuex from 'vuex'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.config.silent = true

describe('ImageList.vue', () => {
  let actions
  let store
  let wrapper

  beforeEach(() => {
    // actions = {
    //   login: jest.fn(),
    // }

    // getters = {
    //   isLoggedIn: () => {
    //     return true
    //   }
    // }

    // store = new Vuex.Store({
    //   getters,
    //   actions
    // })

    // wrapper = shallowMount(Login, { localVue, store })
  })

  it('check title exist 1', () => {
    // const {getByText} = render(Header, {
    //   localVue,
    //   store,
    //   router
    // })

    // const signInButton = getByText('Sign in')
    // const pathAfterClickSignInButton = '/settings'
    // await fireEvent.click(signInButton)
    // expect(actions.login).toHaveBeenCalled()

    // expect(router.currentRoute.path).toMatch(pathAfterClickSignInButton)
  })
})
