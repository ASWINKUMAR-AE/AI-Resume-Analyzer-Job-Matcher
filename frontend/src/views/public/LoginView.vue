<template>
  <div class="auth-page gradient-mesh min-h-screen py-12 flex items-center justify-center">
    <div class="auth-wrapper w-full max-w-md px-4">
      <div class="auth-card card p-8 shadow-xl bg-white">
        <!-- Logo & Header -->
        <div class="auth-header text-center mb-6">
          <div class="logo-icon-box mx-auto mb-3">
            <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
              <polyline points="14 2 14 8 20 8"/>
              <path d="M10 13l2 2 4-4"/>
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-slate-900">Welcome Back</h1>
          <p class="text-slate-600 text-sm mt-1">Sign in to your AI Career & Recruitment account</p>
        </div>

        <!-- Quick Demo Switcher Tabs -->
        <div class="demo-tabs-box mb-6">
          <span class="text-xs font-bold text-indigo-900 block mb-2">⚡ Quick 1-Click Demo Logins:</span>
          <div class="demo-tabs-row">
            <button
              type="button"
              class="btn btn-sm demo-tab"
              :class="{ active: email === 'alex.student@example.com' }"
              @click="setDemo('alex.student@example.com', 'Student@123')"
            >
              👨‍🎓 Student
            </button>
            <button
              type="button"
              class="btn btn-sm demo-tab"
              :class="{ active: email === 'hr@technova.com' }"
              @click="setDemo('hr@technova.com', 'Company@123')"
            >
              🏢 Company
            </button>
            <button
              type="button"
              class="btn btn-sm demo-tab"
              :class="{ active: email === 'admin@airesume.com' }"
              @click="setDemo('admin@airesume.com', 'Admin@123')"
            >
              ⚡ Admin
            </button>
          </div>
        </div>

        <!-- Redirect Notice (if redirected from student/resume, etc.) -->
        <div v-if="route.query.redirect" class="p-3 bg-indigo-50 border border-indigo-200 text-indigo-800 text-xs rounded-lg mb-4 flex items-center gap-2">
          <span>🔒 Please sign in to access <strong>{{ formatRedirectPath(route.query.redirect) }}</strong>.</span>
        </div>

        <!-- Error Alert -->
        <div v-if="errorMsg" class="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-sm rounded-lg mb-4">
          {{ errorMsg }}
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label class="form-label">Email Address</label>
            <input
              v-model="email"
              type="email"
              required
              class="form-input"
              placeholder="e.g. alex.student@example.com"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              required
              class="form-input"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            class="btn btn-primary w-full py-3 text-base mt-2"
            :disabled="loading"
          >
            {{ loading ? 'Authenticating...' : 'Sign In' }}
          </button>
        </form>

        <!-- Footer link -->
        <div class="auth-footer text-center mt-6 pt-4 border-t border-slate-100">
          <p class="text-sm text-slate-600">
            Don't have an account?
            <router-link to="/register" class="text-indigo-600 font-semibold hover:underline">
              Create an account
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const authStore = useAuthStore()
const toastStore = useToastStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref(null)

const setDemo = (demoEmail, demoPw) => {
  email.value = demoEmail
  password.value = demoPw
  errorMsg.value = null
}

const formatRedirectPath = (path) => {
  if (path === '/student/resume') return 'Resume AI & ATS Audit'
  if (path === '/student/dashboard') return 'Student Dashboard'
  if (path === '/student/skills') return 'Skills Matrix'
  return path
}

const handleLogin = async () => {
  if (!email.value || !password.value) return
  loading.value = true
  errorMsg.value = null

  try {
    const res = await authStore.login(email.value, password.value)
    if (res.success) {
      toastStore.success(`Welcome back, ${authStore.userName}!`)
      
      const redirectUrl = route.query.redirect
      if (redirectUrl) {
        router.push(redirectUrl)
      } else if (authStore.isStudent) {
        router.push('/student/dashboard')
      } else if (authStore.isCompany) {
        router.push('/company/dashboard')
      } else if (authStore.isAdmin) {
        router.push('/admin/dashboard')
      } else {
        router.push('/')
      }
    } else {
      errorMsg.value = res.message || 'Invalid email or password'
    }
  } catch (err) {
    errorMsg.value = err.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 72px - 200px);
}

.auth-wrapper {
  max-width: 440px;
  width: 100%;
}

.auth-card {
  border-radius: 20px;
}

.logo-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}

.demo-tabs-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px;
}

.demo-tabs-row {
  display: flex;
  gap: 6px;
}

.demo-tab {
  flex: 1;
  font-size: 0.775rem;
  padding: 6px 4px;
  background: white;
  border: 1px solid #cbd5e1;
  color: #475569;
}
.demo-tab:hover, .demo-tab.active {
  background: #eef2ff;
  border-color: #6366f1;
  color: #4f46e5;
  font-weight: 700;
}
</style>
