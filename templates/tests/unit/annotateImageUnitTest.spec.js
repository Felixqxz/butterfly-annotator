import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import { render, fireEvent } from '@testing-library/vue'
import AnnotateImage from '../../src/components/AnnotateImage.vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import router from "../../src/router/index.js"
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)
Vue.config.silent = true

describe('AnnotateImage.vue', () => {
  let getters
  let store
  let actions
  let wrapper

  beforeEach(() => {
    actions = {
      etchImageData: jest.fn(),
      sendAnnotations: jest.fn()
    }
  
    getters = {
      currentUser: () => {
        return { username: 'josiah', email: 'xxx@ic.ac.uk' }
      }
    }
    
    store = new Vuex.Store({
      getters,
      actions
    })

    // wrapper = shallowMount(AnnotateImage, { localVue, store })
  })

  it('test route redirecting after clicking "Back to bank" button', async () => {
    // const {getByText} = render(AnnotateImage, {
    //   localVue,
    //   store,
    //   router,
    //   data() {
    //     return {
    //       bankId: 1
    //     }
    //   },
    // })

    // const backToBankButton = getByText('Back to bank')
    // const pathAfterClickProfileButton = '/bank/' + wrapper.vm.bankId
    // console.log(pathAfterClickProfileButton)
    // await fireEvent.click(backToBankButton)
    // expect(router.currentRoute.path).toMatch(pathAfterClickProfileButton)
  })
})