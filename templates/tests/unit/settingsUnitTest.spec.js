import { mount, createLocalVue } from '@vue/test-utils'
import { render, fireEvent } from '@testing-library/vue'
import Settings from '../../src/components/Settings.vue'
import Vuex from 'vuex'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.config.silent = true

describe('Settings.vue', () => {
  let getters
  let store
  let wrapper

  beforeEach(() => {
    getters = {
      currentUser: () => {
        return { username: 'josiah', email: 'xxx@ic.ac.uk' }
      }
    }
    store = new Vuex.Store({
      getters
    })
    wrapper = mount(Settings, { localVue, store })
  })

  it('test getters: {currentUser: currentUser} ', async () => {
    // const {getByText} = render(Settings, {
    //   localVue,
    //   store
    // })

    // const userInput = wrapper.find('#username-input')       
    // console.log(userInput.element.id)
    // console.log(userInput.element.value)
    // // await fireEvent.click(userInput)
    // expect(userInput.element.value).toBe(store.getters.currentUser.username)
    // expect(userInput.element.value).not.toBe(store.getters.currentUser.email)

    // const emailInput = wrapper.find('#email-input')   
    // expect(emailInput.element.value).toBe(store.getters.currentUser.email)
  })
})
