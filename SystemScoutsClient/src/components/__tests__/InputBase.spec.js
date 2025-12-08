/**
 * Unit tests for InputBase component
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import InputBase from '../InputBase.vue'

describe('InputBase', () => {
  it('renders input field', () => {
    const wrapper = mount(InputBase, {
      props: {
        modelValue: '',
        label: 'Test Input',
      },
    })

    expect(wrapper.find('input').exists()).toBe(true)
    expect(wrapper.text()).toContain('Test Input')
  })

  it('updates modelValue on input', async () => {
    const wrapper = mount(InputBase, {
      props: {
        modelValue: '',
      },
    })

    const input = wrapper.find('input')
    await input.setValue('new value')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['new value'])
  })

  it('displays error message when provided', () => {
    const wrapper = mount(InputBase, {
      props: {
        modelValue: '',
        error: 'This field is required',
      },
    })

    expect(wrapper.text()).toContain('This field is required')
  })

  it('shows required indicator when required', () => {
    const wrapper = mount(InputBase, {
      props: {
        modelValue: '',
        label: 'Test Input',
        required: true,
      },
    })

    expect(wrapper.html()).toContain('*')
  })

  it('applies input type correctly', () => {
    const wrapper = mount(InputBase, {
      props: {
        modelValue: '',
        type: 'email',
      },
    })

    const input = wrapper.find('input')
    expect(input.attributes('type')).toBe('email')
  })

  it('is disabled when disabled prop is true', () => {
    const wrapper = mount(InputBase, {
      props: {
        modelValue: '',
        disabled: true,
      },
    })

    const input = wrapper.find('input')
    expect(input.attributes('disabled')).toBeDefined()
  })
})
