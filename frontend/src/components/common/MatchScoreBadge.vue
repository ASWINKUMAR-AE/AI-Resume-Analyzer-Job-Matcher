<template>
  <div class="match-badge-container">
    <div
      class="match-badge"
      :class="badgeClass"
      :title="`AI Match Score: ${score || 0}%`"
    >
      <span class="match-icon">⚡</span>
      <span class="match-score-value">{{ formattedScore }}%</span>
      <span v-if="showLabel" class="match-label">Match</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: {
    type: [Number, String],
    default: 0
  },
  showLabel: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'md' // sm, md, lg
  }
})

const numericScore = computed(() => {
  const num = parseFloat(props.score)
  return isNaN(num) ? 0 : num
})

const formattedScore = computed(() => {
  return Math.round(numericScore.value)
})

const badgeClass = computed(() => {
  const s = numericScore.value
  let tone = 'match-low'
  if (s >= 85) tone = 'match-high'
  else if (s >= 70) tone = 'match-good'
  else if (s >= 50) tone = 'match-fair'
  return `${tone} size-${props.size}`
})
</script>

<style scoped>
.match-badge-container {
  display: inline-flex;
}

.match-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-heading);
  font-weight: 700;
  border-radius: 9999px;
  line-height: 1;
  transition: all 0.2s ease;
}

.size-sm {
  padding: 3px 8px;
  font-size: 0.775rem;
}
.size-sm .match-icon {
  font-size: 10px;
}

.size-md {
  padding: 5px 12px;
  font-size: 0.875rem;
}

.size-lg {
  padding: 8px 18px;
  font-size: 1.15rem;
}

.match-high {
  background: #ecfdf5;
  color: #047857;
  border: 1.5px solid #10b981;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);
}

.match-good {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1.5px solid #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.match-fair {
  background: #fffbeb;
  color: #b45309;
  border: 1.5px solid #f59e0b;
}

.match-low {
  background: #fff1f2;
  color: #be123c;
  border: 1.5px solid #f43f5e;
}
</style>
