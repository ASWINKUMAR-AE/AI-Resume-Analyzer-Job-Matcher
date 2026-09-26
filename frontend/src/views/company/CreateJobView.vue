<template>
  <div class="create-job-page py-8 bg-slate-50 min-h-screen">
    <div class="container max-w-3xl">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">{{ isEdit ? 'Edit Job Posting' : 'Create New Job Posting' }}</h1>
          <p class="text-slate-600 text-sm mt-1">
            Publish your tech vacancy. Our AI will automatically extract features and calculate applicant compatibility scores.
          </p>
        </div>
        <router-link to="/company/jobs" class="btn btn-secondary btn-sm">
          ← Back to Jobs
        </router-link>
      </div>

      <form class="card p-8 shadow-sm flex flex-col gap-6" @submit.prevent="handleSubmit">
        <!-- Title & Job Type -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">Job Title *</label>
            <input
              v-model="form.title"
              type="text"
              required
              class="form-input"
              placeholder="e.g. Senior Python & Vue Engineer"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Job Type *</label>
            <select v-model="form.job_type" class="form-select" required>
              <option value="Full Time">Full Time</option>
              <option value="Part Time">Part Time</option>
              <option value="Internship">Internship</option>
              <option value="Contract">Contract</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
            </select>
          </div>
        </div>

        <!-- Location & Experience Required -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">Location</label>
            <input
              v-model="form.location"
              type="text"
              class="form-input"
              placeholder="e.g. San Francisco, CA (Hybrid) or Remote"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Experience Required</label>
            <input
              v-model="form.experience_required"
              type="text"
              class="form-input"
              placeholder="e.g. 2-4 years"
            />
          </div>
        </div>

        <!-- Skills: Required & Preferred -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">Required Skills (Comma-separated) *</label>
            <input
              v-model="form.skills"
              type="text"
              required
              class="form-input"
              placeholder="Python, Flask, Vue.js, MySQL, REST API, Git"
            />
            <span class="text-xs text-slate-500 mt-1 block">Used as primary targets in the AI matching formula.</span>
          </div>

          <div class="form-group">
            <label class="form-label">Preferred Skills (Optional)</label>
            <input
              v-model="form.preferred_skills"
              type="text"
              class="form-input"
              placeholder="Docker, AWS, Kubernetes, TypeScript"
            />
          </div>
        </div>

        <!-- Salary Min / Max & Deadline -->
        <div class="grid grid-cols-3 gap-4">
          <div class="form-group">
            <label class="form-label">Min Annual Salary ($)</label>
            <input
              v-model.number="form.salary_min"
              type="number"
              min="0"
              step="1000"
              class="form-input"
              placeholder="85000"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Max Annual Salary ($)</label>
            <input
              v-model.number="form.salary_max"
              type="number"
              min="0"
              step="1000"
              class="form-input"
              placeholder="120000"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Application Deadline</label>
            <input
              v-model="form.application_deadline"
              type="date"
              class="form-input"
            />
          </div>
        </div>

        <!-- Description -->
        <div class="form-group">
          <label class="form-label">Full Job Description *</label>
          <textarea
            v-model="form.description"
            rows="6"
            required
            class="form-textarea"
            placeholder="Detailed overview of company mission, role responsibilities, daily workflow, and tech stack..."
          ></textarea>
        </div>

        <!-- Requirements -->
        <div class="form-group">
          <label class="form-label">Requirements & Responsibilities</label>
          <textarea
            v-model="form.requirements"
            rows="4"
            class="form-textarea"
            placeholder="Qualifications, academic background, preferred certifications, and day-to-day deliverables..."
          ></textarea>
        </div>

        <!-- Status -->
        <div class="form-group">
          <label class="form-label">Listing Status</label>
          <select v-model="form.status" class="form-select w-48">
            <option value="active">Active (Visible on Job Board)</option>
            <option value="closed">Closed</option>
            <option value="draft">Draft</option>
          </select>
        </div>

        <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
          <router-link to="/company/jobs" class="btn btn-secondary">Cancel</router-link>
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? 'Publishing...' : (isEdit ? 'Save Changes' : 'Publish Job Listing') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { jobsApi } from '@/api'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const router = useRouter()
const toastStore = useToastStore()

const jobId = computed(() => route.params.id)
const isEdit = computed(() => !!jobId.value)
const submitting = ref(false)

const form = reactive({
  title: '',
  job_type: 'Full Time',
  location: 'San Francisco, CA (Hybrid)',
  experience_required: '1-3 years',
  skills: '',
  preferred_skills: '',
  salary_min: 80000,
  salary_max: 115000,
  application_deadline: '',
  description: '',
  requirements: '',
  status: 'active'
})

const fetchJob = async () => {
  if (!isEdit.value) return
  try {
    const res = await jobsApi.getJobDetail(jobId.value)
    if (res.success && res.data) {
      Object.assign(form, res.data)
      if (form.application_deadline) {
        form.application_deadline = form.application_deadline.split('T')[0]
      }
    }
  } catch (err) {
    toastStore.error('Failed to load job details for editing')
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (isEdit.value) {
      const res = await jobsApi.updateJob(jobId.value, form)
      if (res.success) {
        toastStore.success('Job updated successfully!')
        router.push('/company/jobs')
      }
    } else {
      const res = await jobsApi.createJob(form)
      if (res.success) {
        toastStore.success('Job published successfully!')
        router.push('/company/jobs')
      }
    }
  } catch (err) {
    toastStore.error(err.message || 'Action failed')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchJob()
})
</script>

<style scoped>
@media (max-width: 768px) {
  .grid-cols-2, .grid-cols-3 {
    grid-template-columns: 1fr;
  }
}
</style>
