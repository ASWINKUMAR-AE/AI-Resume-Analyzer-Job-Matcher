import { defineStore } from 'pinia'
import apiClient from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    profile: null,
    loading: false
  }),
  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    role: (state) => state.user?.role || null,
    isStudent: (state) => state.user?.role === 'student',
    isCompany: (state) => state.user?.role === 'company',
    isAdmin: (state) => state.user?.role === 'admin',
    userName: (state) => state.user?.name || 'User',
    userEmail: (state) => state.user?.email || ''
  },
  actions: {
    async login(email, password) {
      this.loading = true
      try {
        const res = await apiClient.post('/auth/login', { email, password })
        if (res.success && res.data) {
          this.token = res.data.token
          this.user = res.data.user
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('user', JSON.stringify(res.data.user))
          await this.fetchProfile()
          return { success: true, user: res.data.user }
        }
        return { success: false, message: res.message || 'Login failed' }
      } catch (err) {
        return { success: false, message: err.message }
      } finally {
        this.loading = false
      }
    },

    async register(data) {
      this.loading = true
      try {
        const res = await apiClient.post('/auth/register', data)
        if (res.success && res.data) {
          this.token = res.data.token
          this.user = res.data.user
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('user', JSON.stringify(res.data.user))
          await this.fetchProfile()
          return { success: true, user: res.data.user }
        }
        return { success: false, message: res.message || 'Registration failed' }
      } catch (err) {
        return { success: false, message: err.message }
      } finally {
        this.loading = false
      }
    },

    async fetchProfile() {
      if (!this.token) return
      try {
        const res = await apiClient.get('/auth/me')
        if (res.success && res.data) {
          this.user = res.data.user
          this.profile = res.data.profile
          localStorage.setItem('user', JSON.stringify(res.data.user))
        }
      } catch (err) {
        console.error('Failed to fetch profile:', err)
      }
    },

    logout() {
      try {
        apiClient.post('/auth/logout').catch(() => {})
      } catch (e) {}
      this.token = null
      this.user = null
      this.profile = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
