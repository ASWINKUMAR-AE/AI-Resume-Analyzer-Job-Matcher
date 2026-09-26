<template>
  <div class="auth-page gradient-mesh min-h-screen py-12 flex items-center justify-center">
    <div class="container max-w-xl">
      <div class="auth-card card p-8 shadow-xl">
        <!-- Logo & Header -->
        <div class="auth-header text-center mb-6">
          <div class="logo-icon-box mx-auto mb-3">
            <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
              <polyline points="14 2 14 8 20 8"/>
              <path d="M10 13l2 2 4-4"/>
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-slate-900">Create Your Account</h1>
          <p class="text-slate-600 text-sm mt-1">Join the intelligent AI career and matching network</p>
        </div>

        <!-- Role Selector Tabs -->
        <div class="role-selector-tabs mb-6">
          <button
            type="button"
            class="role-tab"
            :class="{ active: role === 'student' }"
            @click="role = 'student'"
          >
            👨‍🎓 I am a Student / Job Seeker
          </button>
          <button
            type="button"
            class="role-tab"
            :class="{ active: role === 'company' }"
            @click="role = 'company'"
          >
            🏢 I am an Employer / Company
          </button>
        </div>

        <!-- Error Alert -->
        <div v-if="errorMsg" class="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-sm rounded-lg mb-4">
          {{ errorMsg }}
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="handleRegister">
          <!-- Common Base Fields -->
          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">{{ role === 'company' ? 'Company Name' : 'Full Name' }} *</label>
              <input
                v-model="form.name"
                type="text"
                required
                class="form-input"
                :placeholder="role === 'company' ? 'Acme Technologies Inc.' : 'Jane Doe'"
              />
            </div>

            <div class="form-group">
              <label class="form-label">{{ role === 'company' ? 'Official Work Email' : 'Email Address' }} *</label>
              <input
                v-model="form.email"
                type="email"
                required
                class="form-input"
                :placeholder="role === 'company' ? 'careers@acme.com' : 'jane@example.com'"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">Password (Min 6 chars) *</label>
              <input
                v-model="form.password"
                type="password"
                required
                minlength="6"
                class="form-input"
                placeholder="••••••••"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Confirm Password *</label>
              <input
                v-model="form.confirmPassword"
                type="password"
                required
                minlength="6"
                class="form-input"
                placeholder="••••••••"
              />
            </div>
          </div>

          <!-- Student Specific Fields -->
          <template v-if="role === 'student'">
            <div class="grid grid-cols-2 gap-4">
              <div class="form-group">
                <label class="form-label">College / University</label>
                <input
                  v-model="form.college"
                  type="text"
                  class="form-input"
                  placeholder="e.g. Stanford University"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Degree & Field</label>
                <input
                  v-model="form.degree"
                  type="text"
                  class="form-input"
                  placeholder="e.g. B.S. in Computer Science"
                />
              </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div class="form-group">
                <label class="form-label">Graduation Year</label>
                <input
                  v-model.number="form.graduation_year"
                  type="number"
                  min="2000"
                  max="2035"
                  class="form-input"
                  placeholder="2025"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Experience Level</label>
                <select v-model="form.experience" class="form-select">
                  <option value="Entry Level (0-1 yrs)">Entry Level (0-1 yrs)</option>
                  <option value="Junior (1-2 yrs)">Junior (1-2 yrs)</option>
                  <option value="Mid-Level (3-5 yrs)">Mid-Level (3-5 yrs)</option>
                  <option value="Senior (5+ yrs)">Senior (5+ yrs)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Location</label>
                <input
                  v-model="form.location"
                  type="text"
                  class="form-input"
                  placeholder="City, State"
                />
              </div>
            </div>
          </template>

          <!-- Company Specific Fields -->
          <template v-else-if="role === 'company'">
            <div class="grid grid-cols-2 gap-4">
              <div class="form-group">
                <label class="form-label">Industry</label>
                <input
                  v-model="form.industry"
                  type="text"
                  class="form-input"
                  placeholder="e.g. Software & Cloud AI"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Website URL</label>
                <input
                  v-model="form.website"
                  type="url"
                  class="form-input"
                  placeholder="https://example.com"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="form-group">
                <label class="form-label">Headquarters / Location</label>
                <input
                  v-model="form.location"
                  type="text"
                  class="form-input"
                  placeholder="e.g. San Francisco, CA (Hybrid)"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Contact Phone</label>
                <input
                  v-model="form.phone"
                  type="text"
                  class="form-input"
                  placeholder="+1-555-0199"
                />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Company Description</label>
              <textarea
                v-model="form.description"
                class="form-textarea"
                rows="3"
                placeholder="Brief description of what your company builds..."
              ></textarea>
            </div>
          </template>

          <button
            type="submit"
            class="btn btn-primary w-full py-3 text-base mt-4"
            :disabled="loading"
          >
            {{ loading ? 'Creating Account...' : 'Complete Registration' }}
          </button>
        </form>

        <!-- Footer link -->
        <div class="auth-footer text-center mt-6 pt-4 border-t border-slate-100">
          <p class="text-sm text-slate-600">
            Already have an account?
            <router-link to="/login" class="text-indigo-600 font-semibold hover:underline">
              Sign In
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const authStore = useAuthStore()
const toastStore = useToastStore()
const router = useRouter()

const role = ref('student')
const loading = ref(false)
const errorMsg = ref(null)

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  phone: '',
  location: '',
  college: '',
  degree: '',
  graduation_year: 2025,
  experience: 'Entry Level (0-1 yrs)',
  industry: '',
  website: '',
  description: ''
})

const handleRegister = async () => {
  errorMsg.value = null

  if (form.password !== form.confirmPassword) {
    errorMsg.value = 'Passwords do not match.'
    return
  }

  loading.value = true

  const payload = {
    role: role.value,
    name: form.name.trim(),
    email: form.email.trim(),
    password: form.password,
    phone: form.phone,
    location: form.location,
    college: form.college,
    degree: form.degree,
    graduation_year: form.graduation_year,
    experience: form.experience,
    company_name: form.name.trim(),
    industry: form.industry,
    website: form.website,
    description: form.description
  }

  try {
    const res = await authStore.register(payload)
    if (res.success) {
      toastStore.success(`Account created successfully! Welcome, ${authStore.userName}!`)
      if (role.value === 'student') router.push('/student/dashboard')
      else if (role.value === 'company') router.push('/company/dashboard')
    } else {
      errorMsg.value = res.message || 'Registration failed'
    }
  } catch (err) {
    errorMsg.value = err.message || 'Registration failed'
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
}

.auth-card {
  border-radius: 20px;
}

.role-selector-tabs {
  display: flex;
  background: #f1f5f9;
  border-radius: 12px;
  padding: 4px;
  gap: 4px;
}

.role-tab {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px 12px;
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  border-radius: 9px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.role-tab:hover {
  color: #1e293b;
}

.role-tab.active {
  background: white;
  color: #4f46e5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>
