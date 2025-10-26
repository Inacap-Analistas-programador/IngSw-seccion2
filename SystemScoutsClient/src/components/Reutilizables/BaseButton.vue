<template>
  <button
    class="base-button"
    :class="[sizeClass, variantClass, { 'is-disabled': disabled, 'is-block': block }]"
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
      validator: (val) => [
        "primary",
        "secondary",
        "success",
        "info",
        "warning",
        "danger",
        "neutral",
        "outline",
        "ghost"
      ].includes(val),
    },
    size: {
      type: String,
      default: "md",
      validator: (val) => ["sm", "md", "lg", "xl"].includes(val),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    block: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sizeClass() {
      switch (this.size) {
        case "sm": return "btn--sm";
        case "lg": return "btn--lg";
        case "xl": return "btn--xl";
        default:   return "btn--md";
      }
    },
    variantClass() {
      switch (this.variant) {
        case "secondary": return "btn--secondary";
        case "success": return "btn--success";
        case "info": return "btn--info";
        case "warning": return "btn--warning";
        case "danger": return "btn--danger";
        case "neutral": return "btn--neutral";
        case "outline": return "btn--outline";
        case "ghost": return "btn--ghost";
        default: return "btn--primary";
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

<style scoped>
.base-button {
  --btn-bg: var(--color-primary);
  --btn-fg: #ffffff;
  --btn-bg-hover: var(--color-primary-hover);
  --btn-ring: var(--ring-color);
  --btn-border: transparent;

  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--btn-radius);
  border: 1px solid var(--btn-border);
  background: var(--btn-bg);
  color: var(--btn-fg);
  font-weight: var(--btn-font-weight);
  line-height: 1.2;
  cursor: pointer;
  transition: background-color .15s ease, box-shadow .15s ease, transform .12s ease, border-color .15s ease, color .15s ease;
  box-shadow: var(--btn-shadow);
}

.base-button:hover { 
  background: var(--btn-bg-hover); 
  box-shadow: var(--btn-shadow-hover);
  transform: translateY(-1px);
}
.base-button:active { transform: translateY(0); }
.base-button:focus { outline: none; box-shadow: 0 0 0 3px var(--btn-ring); }
.base-button.is-disabled { opacity: .6; cursor: not-allowed; box-shadow: none; }
.base-button.is-block { width: 100%; }

/* Sizes */
.btn--sm { padding: 6px 10px; font-size: 12px; }
.btn--md { padding: 8px 14px; font-size: 14px; }
.btn--lg { padding: 10px 16px; font-size: 15px; }
.btn--xl { padding: 12px 18px; font-size: 16px; }

/* Variants using design tokens */
.btn--primary {
  --btn-bg: var(--color-primary);
  --btn-fg: #fff;
  --btn-bg-hover: var(--color-primary-hover);
  --btn-ring: var(--ring-color);
}

.btn--secondary {
  --btn-bg: var(--color-secondary);
  --btn-fg: #fff;
  --btn-bg-hover: var(--color-secondary-hover);
  --btn-ring: var(--ring-color-weak);
}

.btn--success {
  --btn-bg: var(--color-success);
  --btn-fg: #fff;
  --btn-bg-hover: var(--color-success-hover);
}

.btn--info {
  --btn-bg: var(--color-info);
  --btn-fg: #fff;
  --btn-bg-hover: var(--color-info-hover);
}

.btn--warning {
  --btn-bg: var(--color-warning);
  --btn-fg: #111;
  --btn-bg-hover: var(--color-warning-hover);
}

.btn--danger {
  --btn-bg: var(--color-danger);
  --btn-fg: #fff;
  --btn-bg-hover: var(--color-danger-hover);
}

.btn--neutral {
  --btn-bg: #e5e7eb;
  --btn-fg: #111827;
  --btn-bg-hover: #d1d5db;
  --btn-ring: var(--ring-color-weak);
}

.btn--outline {
  --btn-bg: transparent;
  --btn-fg: var(--color-primary);
  --btn-border: var(--color-primary);
  --btn-bg-hover: rgba(33, 78, 156, 0.06);
}

.btn--ghost {
  --btn-bg: transparent;
  --btn-fg: var(--color-text);
  --btn-bg-hover: rgba(17, 24, 39, 0.06);
  --btn-border: transparent;
  box-shadow: none;
}
</style>
