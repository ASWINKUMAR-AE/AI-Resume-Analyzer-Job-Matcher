<template>
  <div class="loader-container" :class="{ 'full-screen': fullScreen }">
    <div class="loader-radar">
      <div class="radar-pulse"></div>
      <div class="radar-core">
        <svg class="w-6 h-6 text-white animate-spin-slow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" stroke-opacity="0.25"/>
          <path d="M12 2a10 10 0 0 1 10 10" stroke="#ffffff"/>
        </svg>
      </div>
    </div>
    <p v-if="text" class="loader-text">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: 'AI Processing...'
  },
  fullScreen: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  gap: 16px;
}

.loader-container.full-screen {
  min-height: 60vh;
}

.loader-radar {
  position: relative;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar-pulse {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.25);
  animation: pulseGlow 1.8s infinite ease-out;
}

.radar-core {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
}

.radar-core svg {
  width: 22px;
  height: 22px;
}

.loader-text {
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 600;
  color: #475569;
}
</style>
