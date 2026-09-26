<template>
  <div class="student-profile-page py-8 bg-slate-50 min-h-screen">
    <div class="container max-w-3xl">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Student Profile & Preferences</h1>
          <p class="text-slate-600 text-sm mt-1">Manage your academic credentials, experience, and contact links.</p>
        </div>
      </div>

      <Loader v-if="loading" text="Loading profile details..." />

      <form v-else class="card p-8 shadow-sm flex flex-col gap-6" @submit.prevent="handleSave">
        <!-- Basic Info -->
        <div>
          <h3 class="text-base font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100">Personal Information</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">Full Name *</label>
              <input v-model="profile.name" type="text" required class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Email Address (Read-only)</label>
              <input v-model="profile.email" type="email" disabled class="form-input bg-slate-100 cursor-not-allowed" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">Phone Number</label>
              <input v-model="profile.phone" type="text" class="form-input" placeholder="+1-555-0123" />
            </div>
            <div class="form-group">
              <label class="form-label">Location / City</label>
              <input v-model="profile.location" type="text" class="form-input" placeholder="San Francisco, CA" />
            </div>
          </div>
        </div>

        <!-- Academic & Experience Info -->
        <div>
          <h3 class="text-base font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100">Education & Experience</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">College / University</label>
              <input v-model="profile.college" type="text" class="form-input" placeholder="Stanford University" />
            </div>
            <div class="form-group">
              <label class="form-label">Degree & Major</label>
              <input v-model="profile.degree" type="text" class="form-input" placeholder="B.S. in Computer Science" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">Graduation Year</label>
              <input v-model.number="profile.graduation_year" type="number" min="2000" max="2035" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Experience Level</label>
              <input v-model="profile.experience" type="text" class="form-input" placeholder="1-2 years" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Bio / Career Summary</label>
            <textarea v-model="profile.bio" class="form-textarea" rows="3" placeholder="Brief statement about your career goals..."></textarea>
          </div>
        </div>

        <!-- Social & Portfolio Links -->
        <div>
          <h3 class="text-base font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100">Professional Profile Links</h3>
          <div class="grid grid-cols-3 gap-4">
            <div class="form-group">
              <label class="form-label">LinkedIn URL</label>
              <input v-model="profile.linkedin_url" type="url" class="form-input" placeholder="https://linkedin.com/in/..." />
            </div>
            <div class="form-group">
              <label class="form-label">GitHub URL</label>
              <input v-model="profile.github_url" type="url" class="form-input" placeholder="https://github.com/..." />
            </div>
            <div class="form-group">
              <label class="form-label">Portfolio Website</label>
              <input v-model="profile.portfolio_url" type="url" class="form-input" placeholder="https://myportfolio.dev" />
            </div>
          </div>
        </div>

        <div class="flex justify-end pt-4 border-t border-slate-100">
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Saving Profile...' : 'Save Changes' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { studentApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import Loader from '@/components/common/Loader.vue'

const toastStore = useToastStore()
const profile = ref({})
const loading = ref(true)
const saving = ref(false)

const fetchProfile = async () => {
  loading.value = true
  try {
    const res = await studentApi.getProfile()
    if (res.success && res.data) {
      profile.value = res.data
    }
  } catch (err) {
    toastStore.error('Failed to load profile')
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    const res = await studentApi.updateProfile(profile.value)
    if (res.success) {
      toastStore.success('Profile updated successfully!')
    }
  } catch (err) {
    toastStore.error(err.message)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
@media (max-width: 768px) {
  .grid-cols-2, .grid-cols-3 {
    grid-template-columns: 1fr;
  }
}
</style>
