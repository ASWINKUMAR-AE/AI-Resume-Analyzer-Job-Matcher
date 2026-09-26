<template>
  <div class="company-dashboard py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <!-- Header Banner -->
      <div class="welcome-banner card card-glass p-8 mb-8 flex items-center justify-between flex-wrap gap-4">
        <div>
          <div class="welcome-badge">🏢 Employer Portal</div>
          <h1 class="welcome-title">Employer Dashboard</h1>
          <p class="welcome-subtitle">Manage open positions, review AI-ranked candidates, and streamline your hiring pipeline.</p>
        </div>
        <router-link to="/company/jobs/create" class="btn btn-primary">
          + Post New Job
        </router-link>
      </div>

      <Loader v-if="loading" text="Loading employer metrics..." />

      <template v-else>
        <!-- Stat Cards Grid -->
        <div class="stats-grid mb-8">
          <div class="stat-card card p-6">
            <div class="stat-icon bg-indigo-50 text-indigo-600">💼</div>
            <div>
              <div class="stat-val">{{ dashboardData?.stats?.total_jobs || 0 }}</div>
              <div class="stat-lbl">Active Jobs</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-cyan-50 text-cyan-600">👥</div>
            <div>
              <div class="stat-val">{{ dashboardData?.stats?.total_applications || 0 }}</div>
              <div class="stat-lbl">Total Applicants</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-emerald-50 text-emerald-600">⭐</div>
            <div>
              <div class="stat-val">{{ dashboardData?.stats?.shortlisted || 0 }}</div>
              <div class="stat-lbl">Shortlisted</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-purple-50 text-purple-600">⚡</div>
            <div>
              <div class="stat-val">{{ dashboardData?.stats?.avg_match_score || 0 }}%</div>
              <div class="stat-lbl">Avg Match Score</div>
            </div>
          </div>
        </div>

        <!-- Recent Applicants Table -->
        <div class="card overflow-hidden mb-8">
          <div class="p-6 border-b border-slate-100 flex items-center justify-between">
            <h3 class="text-lg font-bold text-slate-900">Recent Candidate Applications</h3>
            <router-link to="/company/applicants" class="text-sm text-indigo-600 font-semibold hover:underline">
              View All Applicants →
            </router-link>
          </div>

          <div v-if="dashboardData?.recent_applications && dashboardData.recent_applications.length > 0" class="table-responsive">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
                  <th class="p-4">Candidate</th>
                  <th class="p-4">Applied Role</th>
                  <th class="p-4">AI Match</th>
                  <th class="p-4">Experience</th>
                  <th class="p-4">Status</th>
                  <th class="p-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-sm">
                <tr v-for="app in dashboardData.recent_applications" :key="app.id" class="hover:bg-slate-50/80 transition">
                  <td class="p-4">
                    <strong class="text-slate-900 block">{{ app.candidate_name }}</strong>
                    <span class="text-xs text-slate-500">{{ app.candidate_email }}</span>
                  </td>
                  <td class="p-4 font-semibold text-slate-700">
                    {{ app.job_title }}
                  </td>
                  <td class="p-4">
                    <MatchScoreBadge :score="app.match_score" size="sm" />
                  </td>
                  <td class="p-4 text-xs text-slate-600">
                    {{ app.degree }} • {{ app.experience || '1-2 yrs' }}
                  </td>
                  <td class="p-4">
                    <select
                      v-model="app.status"
                      class="form-select text-xs py-1 px-2 w-auto"
                      @change="updateStatus(app.id, app.status)"
                    >
                      <option value="Applied">Applied</option>
                      <option value="Under Review">Under Review</option>
                      <option value="Shortlisted">Shortlisted</option>
                      <option value="Interview">Interview</option>
                      <option value="Selected">Selected</option>
                      <option value="Rejected">Rejected</option>
                    </select>
                  </td>
                  <td class="p-4 text-right">
                    <router-link to="/company/applicants" class="btn btn-secondary btn-sm text-xs">
                      Review
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="text-center p-8 text-slate-500 text-sm">
            No applicants received yet. Post jobs to start receiving AI-matched applications!
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { companyApi, applicationsApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import MatchScoreBadge from '@/components/common/MatchScoreBadge.vue'
import Loader from '@/components/common/Loader.vue'

const toastStore = useToastStore()
const dashboardData = ref(null)
const loading = ref(true)

const fetchDashboard = async () => {
  loading.value = true
  try {
    const res = await companyApi.getDashboard()
    if (res.success) {
      dashboardData.value = res.data
    }
  } catch (err) {
    toastStore.error('Failed to load employer dashboard')
  } finally {
    loading.value = false
  }
}

const updateStatus = async (appId, newStatus) => {
  try {
    const res = await applicationsApi.updateStatus(appId, newStatus)
    if (res.success) {
      toastStore.success(`Status updated to ${newStatus}`)
    }
  } catch (err) {
    toastStore.error(err.message)
  }
}

onMounted(() => {
  fetchDashboard()
})
</script>

<style scoped>
.welcome-banner {
  border-radius: 20px;
}
.welcome-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #047857;
  background: #ecfdf5;
  padding: 3px 10px;
  border-radius: 999px;
  margin-bottom: 8px;
}
.welcome-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f172a;
}
.welcome-subtitle {
  font-size: 0.95rem;
  color: #475569;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  border-radius: 16px;
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}
.stat-val {
  font-size: 1.6rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.1;
}
.stat-lbl {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.table-responsive {
  overflow-x: auto;
}
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
