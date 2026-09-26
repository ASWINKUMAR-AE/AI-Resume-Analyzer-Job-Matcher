import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: []
  }),
  actions: {
    show(message, type = 'info', duration = 4000) {
      const id = Date.now() + Math.random()
      this.toasts.push({ id, message, type })

      if (duration > 0) {
        setTimeout(() => {
          this.remove(id)
        }, duration)
      }
    },
    success(message, duration = 4000) {
      this.show(message, 'success', duration)
    },
    error(message, duration = 5000) {
      this.show(message, 'error', duration)
    },
    warning(message, duration = 4500) {
      this.show(message, 'warning', duration)
    },
    info(message, duration = 4000) {
      this.show(message, 'info', duration)
    },
    remove(id) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    }
  }
})
