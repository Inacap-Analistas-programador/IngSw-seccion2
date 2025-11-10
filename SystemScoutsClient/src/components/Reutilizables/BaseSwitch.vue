<template>
  <label class="switch-container">
    <input
      type="checkbox"
      :checked="modelValue"
      @change="$emit('update:modelValue', $event.target.checked)"
      class="switch-input"
    />
    <span class="switch-slider"></span>
  </label>
</template>

<script>
export default {
  name: 'BaseSwitch',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.switch-container {
  position: relative;
  display: inline-block;
  width: 52px;
  height: 28px;
  cursor: pointer;
}

.switch-input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.switch-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e1;
  transition: all 0.3s ease;
  border-radius: 34px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.switch-slider::before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: all 0.3s ease;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.switch-input:checked + .switch-slider {
  background-color: #2563eb;
  box-shadow: inset 0 2px 4px rgba(37, 99, 235, 0.3);
}

.switch-input:focus + .switch-slider {
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}

.switch-input:checked + .switch-slider::before {
  transform: translateX(24px);
}

.switch-container:hover .switch-slider {
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.switch-input:checked + .switch-slider:hover {
  background-color: #1d4ed8;
}

.switch-slider:not(.switch-input:checked + .switch-slider):hover {
  background-color: #94a3b8;
}
</style>
