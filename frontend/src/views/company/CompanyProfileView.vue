<template>
  <div class="company-profile-page py-8 bg-slate-50 min-h-screen">
    <div class="container max-w-3xl">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Company Profile & Branding</h1>
          <p class="text-slate-600 text-sm mt-1">Manage your public organization profile, industry, and contact details.</p>
        </div>
      </div>

      <Loader v-if="loading" text="Loading company profile..." />

      <form v-else class="card p-8 shadow-sm flex flex-col gap-6" @submit.prevent="handleSave">
        <!-- Basic Info -->
        <div>
          <h3 class="text-base font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100">Organization Information</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">Company Name *</label>
              <input v-model="profile.company_name" type="text" required class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Official Work Email</label>
              <input v-model="profile.company_email" type="email" class="form-input" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">Industry Domain</label>
              <input v-model="profile.industry" type="text" class="form-input" placeholder="e.g. Software & Cloud AI" />
            </div>
            <div class="form-group">
              <label class="form-label">Headquarters / Location</label>
              <input v-model="profile.location" type="text" class="form-input" placeholder="e.g. San Francisco, CA (Hybrid)" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label">Company Website</label>
              <input v-model="profile.website" type="url" class="form-input" placeholder="https://example.com" />
            </div>
            <div class="form-group">
              <label class="form-label">Contact Phone</label>
              <input v-model="profile.phone" type="text" class="form-input" placeholder="+1-555-0199" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Company Description & Mission</label>
            <textarea v-model="profile.description" rows="4" class="form-textarea" placeholder="Describe your company, products, and culture..."></textarea>
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
import { companyApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import Loader from '@/components/common/Loader.vue'

const toastStore = useToastStore()
const profile = ref({})
const loading = ref(true)
const saving = ref(false)

const fetchProfile = async () => {
  loading.value = true
  try {
    const res = await companyApi.getProfile()
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
    const res = await companyApi.updateProfile(profile.value)
    if (res.success) {
      toastStore.success('Company profile updated successfully!')
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
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>
