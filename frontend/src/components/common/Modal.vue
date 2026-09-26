<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="isOpen" class="modal-backdrop" @click.self="closeOnBackdrop && close()">
        <div class="modal-dialog" :class="'max-w-' + maxWidth">
          <!-- Modal Header -->
          <div class="modal-header">
            <h3 class="modal-title">{{ title }}</h3>
            <button class="modal-close-btn" @click="close" aria-label="Close modal">×</button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <slot></slot>
          </div>

          <!-- Modal Footer -->
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Modal Title'
  },
  maxWidth: {
    type: String,
    default: 'md' // sm, md, lg, xl, 2xl
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-dialog {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid #e2e8f0;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.max-w-sm { max-width: 420px; }
.max-w-md { max-width: 540px; }
.max-w-lg { max-width: 680px; }
.max-w-xl { max-width: 820px; }
.max-w-2xl { max-width: 1000px; }

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.modal-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
}

.modal-close-btn {
  background: transparent;
  border: none;
  font-size: 24px;
  color: #94a3b8;
  cursor: pointer;
  line-height: 1;
  padding: 4px;
}
.modal-close-btn:hover {
  color: #0f172a;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f1f5f9;
  background: #f8fafc;
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.96);
}
</style>
