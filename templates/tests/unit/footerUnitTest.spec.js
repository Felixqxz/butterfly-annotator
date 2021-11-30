import { shallowMount } from '@vue/test-utils'
import Footer from '../../src/components/Footer.vue'
import Vue from 'vue'

Vue.config.silent = true

describe('Footer.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = '2021 Copyright: butterfly-annotator'
    const wrapper = shallowMount(Footer)
    expect(wrapper.text()).toMatch(msg)
  })
})
