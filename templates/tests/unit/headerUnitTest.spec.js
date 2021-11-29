import { createLocalVue, mount } from '@vue/test-utils'
import Header from '../../src/components/Header.vue'
import BootstrapVue, { BDropdownItem } from 'bootstrap-vue';
import Vuex from 'vuex'
import {getters} from '../../src/store/auth';
import sinon from 'sinon'


const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(BootstrapVue)

const store = new Vuex.Store({
    getters: getters
  })


test('trigger demo', async () => {
  const clickHandler = sinon.stub()
  const wrapper = mount(Header, {
    propsData: { clickHandler },
    localVue,
    store
  })

  const buttonArray = wrapper.findAllComponents(BDropdownItem)
  await buttonArray.trigger('click')
  expect(clickHandler.called).toBe(true)
})
