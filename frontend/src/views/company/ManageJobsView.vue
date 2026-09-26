<template>
  <div class="manage-jobs-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Manage Job Postings</h1>
          <p class="text-slate-600 text-sm mt-1">View active vacancies, applicant volumes, and manage listing statuses.</p>
        </div>
        <router-link to="/company/jobs/create" class="btn btn-primary btn-sm">
          + Post New Job
        </router-link>
      </div>

      <Loader v-if="loading" text="Loading company jobs..." />

      <EmptyState
        v-else-if="jobs.length === 0"
        title="No Jobs Posted Yet"
        message="Create your first job vacancy to start receiving AI-matched applications."
        icon="💼"
      >
        <template #action>
          <router-link to="/company/jobs/create" class="btn btn-primary btn-sm">Create Job Listing</router-link>
        </template>
      </EmptyState>

      <!-- Jobs Table -->
      <div v-else class="card overflow-hidden">
        <div class="table-responsive">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
                <th class="p-4">Job Title</th>
                <th class="p-4">Type & Location</th>
                <th class="p-4">Applicants</th>
                <th class="p-4">Status</th>
                <th class="p-4">Created Date</th>
                <th class="p-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-sm">
              <tr v-for="job in jobs" :key="job.id" class="hover:bg-slate-50/80 transition">
                <td class="p-4">
                  <router-link :to="`/jobs/${job.id}`" class="font-bold text-slate-900 hover:text-indigo-600 block">
                    {{ job.title }}
                  </router-link>
                  <span class="text-xs text-slate-500 font-mono">{{ job.skills }}</span>
                </td>
                <td class="p-4 text-xs text-slate-600">
                  <span class="badge badge-primary mr-1">{{ job.job_type }}</span>
                  <span>{{ job.location }}</span>
                </td>
                <td class="p-4">
                  <router-link :to="`/company/applicants?job_id=${job.id}`" class="badge badge-success hover:underline">
                    👥 {{ job.total_applicants || 0 }} applicants
                  </router-link>
                </td>
                <td class="p-4">
                  <span class="badge" :class="job.status === 'active' ? 'badge-success' : 'badge-warning'">
                    {{ job.status }}
                  </span>
                </td>
                <td class="p-4 text-xs text-slate-500">
                  {{ formatDate(job.created_at) }}
                </td>
                <td class="p-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <router-link :to="`/company/jobs/${job.id}/edit`" class="btn btn-secondary btn-sm text-xs">
                      Edit
                    </router-link>
                    <button class="btn btn-danger btn-sm text-xs" @click="handleDelete(job.id)">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { jobsApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import Loader from '@/components/common/Loader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const authStore = useAuthStore()
const toastStore = useToastStore()
const jobs = ref([])
const loading = ref(true)

const fetchJobs = async () => {
  loading.value = true
  try {
    const res = await jobsApi.getJobs({ company_id: authStore.user?.id })
    if (res.success) {
      jobs.value = res.data || []
    }
  } catch (err) {
    toastStore.error(err.message)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (jobId) => {
  if (!confirm('Are you sure you want to delete this job listing?')) return
  try {
    const res = await jobsApi.deleteJob(jobId)
    if (res.success) {
      toastStore.success('Job listing deleted.')
      jobs.value = jobs.value.filter((j) => j.id !== jobId)
    }
  } catch (err) {
    toastStore.error(err.message)
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}
</style>
