import { createLocalVue, mount } from '@vue/test-utils'
import Header from '../../src/components/Header.vue'
import BootstrapVue, { BDropdownItem } from 'bootstrap-vue';
import Vuex from 'vuex'
import {getters} from '../../src/store/auth';


const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(BootstrapVue)

const store = new Vuex.Store({
    getters: getters
  })



it('trigger demo', () => {
  const onClick = jest.fn(),
  wrapper = mount(Header, {
    localVue,
    store,
    listeners: {
      click: onClick
    }
  })
  // expect(wrapper.attributes().id).toBe('foo')
  // expect(wrapper.attributes('id')).toBe('foo')

  const buttonArray = wrapper.findComponent(BDropdownItem)
    // const buttonArray = wrapper.attributes().id
  // const buttonArray = wrapper.get(id = "bdrop1")
  // buttonArray.trigger('click')
  // expect(onClick).toHaveBeenCalled()
  console.log("-------------------", buttonArray)
})