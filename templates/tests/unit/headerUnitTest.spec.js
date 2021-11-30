import { createLocalVue, mount } from '@vue/test-utils'
import Header from '../../src/components/Header.vue'
import BootstrapVue, { BDropdownItem, BFormInput } from 'bootstrap-vue';
import Vuex from 'vuex'
import {getters} from '../../src/store/auth';
import {render, fireEvent} from '@testing-library/vue'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(BootstrapVue)

const store = new Vuex.Store({
    getters: getters
  })



// it('trigger demo', () => {
//   const onClick = jest.fn(),
//   wrapper = mount(Header, {
//     localVue,
//     store,
//     listeners: {
//       click: onClick
//     },
//     stubs: {
//       // used to register custom components
//       'b-form-input': BFormInput,
//       'b-dropdown-item': BDropdownItem,
//     },
//   })
  // expect(wrapper.attributes().id).toBe('foo')
  // expect(wrapper.attributes('id')).toBe('foo')

  // const buttonArray = wrapper.attributes('onclick')
    // const buttonArray = wrapper.attributes().id
  // const buttonArray = wrapper.get(id = "bdrop1")
  // buttonArray.trigger('click')
  // expect(onClick).toHaveBeenCalled()
//   console.log("-------------------", buttonArray)
// })


test('increments value on click', async () => {
  // The render method returns a collection of utilities to query your component.
  const {getByText} = render(Header, {
    localVue,
    store,
  })

  // getByText returns the first matching node for the provided text, and
  // throws an error if no elements match or if more than one match is found.

  const button = getByText('Profile')
  console.log(button)
  // Dispatch a native click event to our button element.
  await fireEvent.click(button)
  // await fireEvent.click(button)

  // getByText('Times clicked: 2')
})

