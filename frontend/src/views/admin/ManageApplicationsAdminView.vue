<template>
  <div class="admin-apps-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Platform Applications Oversight</h1>
          <p class="text-slate-600 text-sm mt-1">Audit all candidate applications, algorithm match scores, and hiring outcomes.</p>
        </div>
      </div>

      <Loader v-if="loading" text="Loading applications..." />

      <div v-else class="card overflow-hidden">
        <div class="table-responsive">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
                <th class="p-4">Candidate</th>
                <th class="p-4">Target Job & Company</th>
                <th class="p-4">AI Match</th>
                <th class="p-4">Resume</th>
                <th class="p-4">Applied Date</th>
                <th class="p-4">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-sm">
              <tr v-for="app in applications" :key="app.id" class="hover:bg-slate-50/80 transition">
                <td class="p-4">
                  <strong class="text-slate-900 block">{{ app.candidate_name }}</strong>
                  <span class="text-xs text-slate-500">{{ app.candidate_email }}</span>
                </td>
                <td class="p-4 font-semibold text-slate-800">
                  {{ app.job_title }}
                  <span class="block text-xs font-normal text-slate-500">{{ app.company_name }}</span>
                </td>
                <td class="p-4">
                  <MatchScoreBadge :score="app.match_score" size="sm" />
                </td>
                <td class="p-4 text-xs text-slate-600">
                  📄 {{ app.resume_file_name }} ({{ app.resume_score }}/100)
                </td>
                <td class="p-4 text-xs text-slate-500">
                  {{ formatDate(app.applied_at) }}
                </td>
                <td class="p-4">
                  <span class="badge badge-primary">{{ app.status }}</span>
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
import MatchScoreBadge from '@/components/common/MatchScoreBadge.vue'
import Loader from '@/components/common/Loader.vue'

const toastStore = useToastStore()
const applications = ref([])
const loading = ref(true)

const fetchApplications = async () => {
  loading.value = true
  try {
    const res = await adminApi.getApplications()
    if (res.success) {
      applications.value = res.data || []
    }
  } catch (err) {
    toastStore.error(err.message)
  } finally {
    loading.value = false
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
  fetchApplications()
})
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}
</style>
