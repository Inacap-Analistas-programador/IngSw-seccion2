<template>
  <div
    class="datacard"
    role="region"
    :aria-label="`Indicador: ${title}`"
    tabindex="0"
  >
    <div class="icon" v-if="$slots.icon" aria-hidden="true">
      <slot name="icon"></slot>
    </div>
    <div class="content">
      <span class="value">{{ value }}</span>
      <span class="title">{{ title }}</span>
      <p v-if="description" class="description">{{ description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataCard",
  props: {
    title: { type: String, required: true },
    value: { type: [String, Number], required: true },
    description: { type: String, default: "" }
  }
}
</script>

<style scoped>
.datacard {
  background: #fff;
  border: 1px solid #d1d8e6;
  border-radius: 10px;
  display: flex;
  align-items: center;
  min-width: 180px;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  margin: 8px 8px 8px 0;
}

.icon {
  font-size: 2.4rem;
  margin-right: 18px;
  color: #2275c9;
  flex-shrink: 0;
}

.content {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #19548a;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.title {
  font-size: 1rem;
  color: #4472a3;
  letter-spacing: 0.2px;
}

.description {
  font-size: 0.85rem;
  color: #6a7d8b;
  margin-top: 4px;
}
</style>
