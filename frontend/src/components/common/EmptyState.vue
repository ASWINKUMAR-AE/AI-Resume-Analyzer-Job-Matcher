<template>
  <div class="empty-state-box">
    <div class="empty-icon-circle">
      <span class="empty-emoji">{{ icon || '📂' }}</span>
    </div>
    <h3 class="empty-title">{{ title }}</h3>
    <p class="empty-description">{{ message }}</p>
    <div v-if="$slots.action" class="empty-action">
      <slot name="action"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'No Items Found'
  },
  message: {
    type: String,
    default: 'There are no records matching your criteria.'
  },
  icon: {
    type: String,
    default: '🔍'
  }
})
</script>

<style scoped>
.empty-state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 48px 24px;
  background: #ffffff;
  border: 1.5px dashed #cbd5e1;
  border-radius: 16px;
  margin: 16px 0;
}

.empty-icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.empty-emoji {
  font-size: 28px;
}

.empty-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 6px;
}

.empty-description {
  font-size: 0.9rem;
  color: #64748b;
  max-width: 400px;
  line-height: 1.5;
  margin-bottom: 18px;
}

.empty-action {
  margin-top: 4px;
}
</style>
