<template>
  <div class="admin-jobs-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Platform Job Listings Oversight</h1>
          <p class="text-slate-600 text-sm mt-1">Audit and moderate all job postings published across the platform.</p>
        </div>
      </div>

      <Loader v-if="loading" text="Loading platform job postings..." />

      <div v-else class="card overflow-hidden">
        <div class="table-responsive">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
                <th class="p-4">Job Title & Company</th>
                <th class="p-4">Type & Location</th>
                <th class="p-4">Total Applicants</th>
                <th class="p-4">Status</th>
                <th class="p-4 text-right">Moderation Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-sm">
              <tr v-for="job in jobs" :key="job.id" class="hover:bg-slate-50/80 transition">
                <td class="p-4">
                  <router-link :to="`/jobs/${job.id}`" class="font-bold text-slate-900 hover:text-indigo-600 block">
                    {{ job.title }}
                  </router-link>
                  <span class="text-xs text-slate-500">{{ job.company_name }} ({{ job.company_email }})</span>
                </td>
                <td class="p-4 text-xs text-slate-600">
                  <span class="badge badge-primary mr-1">{{ job.job_type }}</span>
                  <span>{{ job.location }}</span>
                </td>
                <td class="p-4 text-xs font-bold text-slate-700">
                  {{ job.total_applicants || 0 }} applicants
                </td>
                <td class="p-4">
                  <span class="badge" :class="job.status === 'active' ? 'badge-success' : 'badge-warning'">
                    {{ job.status }}
                  </span>
                </td>
                <td class="p-4 text-right">
                  <button class="btn btn-danger btn-sm text-xs" @click="handleDelete(job.id)">
                    Remove Job
                  </button>
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
import { adminApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import Loader from '@/components/common/Loader.vue'

const toastStore = useToastStore()
const jobs = ref([])
const loading = ref(true)

const fetchJobs = async () => {
  loading.value = true
  try {
    const res = await adminApi.getJobs()
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
  if (!confirm('Are you sure you want to remove this job posting?')) return
  try {
    const res = await adminApi.deleteJob(jobId)
    if (res.success) {
      toastStore.success('Job removed.')
      jobs.value = jobs.value.filter((j) => j.id !== jobId)
    }
  } catch (err) {
    toastStore.error(err.message)
  }
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
