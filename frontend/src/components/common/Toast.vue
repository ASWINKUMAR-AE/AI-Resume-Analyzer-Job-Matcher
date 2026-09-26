<template>
  <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; max-width: 380px; width: 100%; pointer-events: none;">
    <transition-group name="toast">
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="toast-item pointer-events-auto"
        :class="'toast-' + toast.type"
      >
        <div class="toast-icon">
          <span v-if="toast.type === 'success'">✓</span>
          <span v-else-if="toast.type === 'error'">✕</span>
          <span v-else-if="toast.type === 'warning'">⚠</span>
          <span v-else>ℹ</span>
        </div>
        <div class="toast-message">{{ toast.message }}</div>
        <button class="toast-close" @click="toastStore.remove(toast.id)">×</button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'
const toastStore = useToastStore()
</script>

<style scoped>
.toast-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  background: #ffffff;
  color: #1e293b;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.25s ease;
}

.toast-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  line-height: 1.35;
}

.toast-close {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 18px;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}
.toast-close:hover {
  color: #1e293b;
}

.toast-success {
  border-left: 4px solid #10b981;
}
.toast-success .toast-icon {
  background: #ecfdf5;
  color: #059669;
}

.toast-error {
  border-left: 4px solid #ef4444;
}
.toast-error .toast-icon {
  background: #fef2f2;
  color: #dc2626;
}

.toast-warning {
  border-left: 4px solid #f59e0b;
}
.toast-warning .toast-icon {
  background: #fffbeb;
  color: #d97706;
}

.toast-info {
  border-left: 4px solid #6366f1;
}
.toast-info .toast-icon {
  background: #eef2ff;
  color: #4f46e5;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}
</style>
