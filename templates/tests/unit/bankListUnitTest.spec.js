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
  let wrapper

  beforeEach(() => {
    actions = {
      listBanks: jest.fn(),
    }
    store = new Vuex.Store({
      modules: {
        BankList: {
          actions
        }
      }
    })
    wrapper = shallowMount(BankList, { localVue, store })
  })

  it('check title exist', () => {
    const pageTitle = 'Your banks'
    expect(wrapper.text()).toContain(pageTitle)
  })

  it('adding banks', () => {
    let len = wrapper.findAll('availableBanks').length
    expect(wrapper.findAll('availableBanks')).toHaveLength(len)
    wrapper = mount(BankList, {
      props: {
        availableBanks: []
      },
      localVue, 
      store
    })
    expect(wrapper.findAll('availableBanks')).toHaveLength(0)
  })
})
