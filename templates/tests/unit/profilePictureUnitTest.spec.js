import { createLocalVue } from '@vue/test-utils'
import { render, fireEvent } from '@testing-library/vue'
import ProfilePicture from '../../src/components/ProfilePicture.vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)
Vue.config.silent = true

describe('Header.vue', () => {
  let store
  let actions

  beforeEach(() => {
    actions = {
      uploadProfilePicture: jest.fn()
    }
    
    store = new Vuex.Store({
      actions
    })
  })

  it('test “uploadProfilePicture” will be called clicking "OK" button', async () => {
    const {getByText} = render(ProfilePicture, {
      localVue,
      store
    })

    const okButton = getByText('OK')
    await fireEvent.click(okButton)
    expect(actions.uploadProfilePicture).toHaveBeenCalled()
  })
})
