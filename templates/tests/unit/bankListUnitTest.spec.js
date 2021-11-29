import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import BankList from '../../src/components/BankList.vue'
import ImageList from '../../src/components/ImageList.vue'
import {mapActions, mapGetters} from 'vuex'
import Vuex from 'vuex'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(Vuex)
// const router = new VueRouter()

describe('ImageList.vue', () => {
  let actions
  let store

  beforeEach(() => {
    actions = {
      listBanks: jest.fn(),
      // actionInput: jest.fn()
    }
    store = new Vuex.Store({
      modules: {
        BankList: {
          // state: { books: null },
          actions
        }
      }
    })
  })

  it('check title exist', () => {
    const pageTitle = 'Your banks'
    const wrapper = shallowMount(BankList, { localVue, store })
    expect(wrapper.text()).toContain(pageTitle)
  })
})
