<template>
  <button
    :class="[
      'inline-flex items-center justify-center font-medium rounded-lg transition focus:outline-none focus:ring-2',
      sizeClasses,
      variantClasses,
      { 'opacity-50 cursor-not-allowed': disabled }
    ]"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script>
export default {
  name: "BaseButton",
  props: {
    variant: {
      type: String,
      default: "primary",
      validator: (val) => ["primary", "secondary", "danger"].includes(val),
    },
    size: {
      type: String,
      default: "md",
      validator: (val) => ["sm", "md", "lg"].includes(val),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sizeClasses() {
      switch (this.size) {
        case "sm": return "px-2 py-1 text-sm";
        case "lg": return "px-6 py-3 text-lg";
        default:   return "px-4 py-2 text-base";
      }
    },
    variantClasses() {
      switch (this.variant) {
        case "secondary":
          return "bg-gray-200 text-black hover:bg-gray-300 focus:ring-gray-400";
        case "danger":
          return "bg-red-600 text-white hover:bg-red-700 focus:ring-red-400";
        default: // primary
          return "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-400";
      }
    },
  },
  methods: {
    handleClick(event) {
      if (!this.disabled) {
        this.$emit("click", event);
      }
    },
  },
};
</script>
