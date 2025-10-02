<!-- BaseButton.vue -->
<template>
  <button
    :class="[
      'inline-flex items-center justify-center font-medium rounded-lg transition focus:outline-none focus:ring-2',
      sizeClasses,
      variantClasses,
      { 'opacity-50 cursor-not-allowed': disabled || loading }
    ]"
    :disabled="disabled || loading"
    :aria-disabled="disabled || loading"
    @click="handleClick"
  >
    <!-- Loading spinner -->
    <svg
      v-if="loading"
      class="animate-spin h-4 w-4 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
      />
    </svg>

    <!-- Button text -->
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
      validator: (val) =>
        ["primary", "secondary", "danger", "ghost", "link"].includes(val),
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
    loading: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sizeClasses() {
      switch (this.size) {
        case "sm":
          return "px-2 py-1 text-sm";
        case "lg":
          return "px-6 py-3 text-lg";
        default:
          return "px-4 py-2 text-base";
      }
    },
    variantClasses() {
      switch (this.variant) {
        case "secondary":
          return "bg-gray-200 text-black hover:bg-gray-300 focus:ring-gray-400";
        case "danger":
          return "bg-red-600 text-white hover:bg-red-700 focus:ring-red-400";
        case "ghost":
          return "bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-300";
        case "link":
          return "bg-transparent text-blue-600 hover:underline focus:ring-blue-300";
        default: // primary
          return "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-400";
      }
    },
  },
  methods: {
    handleClick(event) {
      if (!this.disabled && !this.loading) {
        this.$emit("click", event);
      }
    },
  },
};
</script>