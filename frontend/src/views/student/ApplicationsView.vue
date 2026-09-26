<template>
  <div class="applications-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Application Tracker</h1>
          <p class="text-slate-600 text-sm mt-1">Track the status of your submitted job applications in real-time.</p>
        </div>
        <router-link to="/jobs" class="btn btn-secondary btn-sm">Find More Jobs</router-link>
      </div>

      <Loader v-if="loading" text="Loading applications..." />

      <EmptyState
        v-else-if="applications.length === 0"
        title="No Applications Submitted"
        message="You have not applied for any roles yet. Browse recommendations and submit your first application!"
        icon="📄"
      >
        <template #action>
          <router-link to="/jobs" class="btn btn-primary btn-sm">Find Matching Jobs</router-link>
        </template>
      </EmptyState>

      <!-- Applications Table -->
      <div v-else class="card overflow-hidden">
        <div class="table-responsive">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
                <th class="p-4">Position & Company</th>
                <th class="p-4">AI Match</th>
                <th class="p-4">Resume Used</th>
                <th class="p-4">Applied Date</th>
                <th class="p-4">Hiring Status</th>
                <th class="p-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-sm">
              <tr v-for="app in applications" :key="app.id" class="hover:bg-slate-50/80 transition">
                <!-- Position & Company -->
                <td class="p-4">
                  <router-link :to="`/jobs/${app.job_id}`" class="font-bold text-slate-900 hover:text-indigo-600 block">
                    {{ app.job_title }}
                  </router-link>
                  <span class="text-xs text-slate-500">{{ app.company_name }} • {{ app.job_location }}</span>
                </td>

                <!-- AI Match -->
                <td class="p-4">
                  <MatchScoreBadge :score="app.match_score" size="sm" />
                </td>

                <!-- Resume Used -->
                <td class="p-4 text-xs text-slate-600">
                  📄 {{ app.resume_file_name }}
                </td>

                <!-- Applied Date -->
                <td class="p-4 text-xs text-slate-500">
                  {{ formatDate(app.applied_at) }}
                </td>

                <!-- Status Badge -->
                <td class="p-4">
                  <span class="status-badge" :class="getStatusClass(app.status)">
                    {{ app.status }}
                  </span>
                </td>

                <!-- Action -->
                <td class="p-4 text-right">
                  <router-link :to="`/jobs/${app.job_id}`" class="btn btn-secondary btn-sm text-xs">
                    View Job
                  </router-link>
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
import { applicationsApi } from '@/api'
import MatchScoreBadge from '@/components/common/MatchScoreBadge.vue'
import Loader from '@/components/common/Loader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const applications = ref([])
const loading = ref(true)

const fetchApplications = async () => {
  loading.value = true
  try {
    const res = await applicationsApi.getStudentApplications()
    if (res.success) {
      applications.value = res.data || []
    }
  } catch (err) {
    console.error('Failed to load student applications:', err)
  } finally {
    loading.value = false
  }
}

const getStatusClass = (status) => {
  switch (status) {
    case 'Shortlisted':
      return 'status-shortlisted'
    case 'Interview':
      return 'status-interview'
    case 'Selected':
      return 'status-selected'
    case 'Under Review':
      return 'status-review'
    case 'Rejected':
      return 'status-rejected'
    default:
      return 'status-applied'
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

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.775rem;
  font-weight: 700;
  text-transform: capitalize;
}

.status-applied {
  background: #eef2ff;
  color: #4f46e5;
  border: 1px solid #c7d2fe;
}

.status-review {
  background: #eff6ff;
  color: #2563eb;
  border: 1px solid #bfdbfe;
}

.status-shortlisted {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.status-interview {
  background: #fdf4ff;
  color: #c026d3;
  border: 1px solid #f5d0fe;
}

.status-selected {
  background: #f0fdf4;
  color: #15803d;
  border: 1.5px solid #86efac;
}

.status-rejected {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}
</style>
