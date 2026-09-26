<template>
  <div class="admin-dashboard py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <!-- Admin Header Banner -->
      <div class="welcome-banner card card-glass p-8 mb-8 flex items-center justify-between flex-wrap gap-4">
        <div>
          <div class="welcome-badge">⚡ Platform Administration</div>
          <h1 class="welcome-title">System & AI Analytics Dashboard</h1>
          <p class="welcome-subtitle">Platform health, user metrics, job postings oversight, and AI processing statistics.</p>
        </div>
        <div class="system-health-pill badge badge-success py-2 px-4 text-xs font-bold">
          ● All Services Operational (XAMPP MySQL & Local AI)
        </div>
      </div>

      <Loader v-if="loading" text="Loading platform administration metrics..." />

      <template v-else>
        <!-- Metric Cards -->
        <div class="stats-grid mb-8">
          <div class="stat-card card p-6">
            <div class="stat-icon bg-indigo-50 text-indigo-600">👥</div>
            <div>
              <div class="stat-val">{{ adminData?.stats?.total_users || 0 }}</div>
              <div class="stat-lbl">Total Users</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-cyan-50 text-cyan-600">👨‍🎓</div>
            <div>
              <div class="stat-val">{{ adminData?.stats?.total_students || 0 }}</div>
              <div class="stat-lbl">Registered Students</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-emerald-50 text-emerald-600">🏢</div>
            <div>
              <div class="stat-val">{{ adminData?.stats?.total_companies || 0 }}</div>
              <div class="stat-lbl">Companies</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-purple-50 text-purple-600">💼</div>
            <div>
              <div class="stat-val">{{ adminData?.stats?.total_jobs || 0 }}</div>
              <div class="stat-lbl">Job Listings</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-amber-50 text-amber-600">📄</div>
            <div>
              <div class="stat-val">{{ adminData?.stats?.total_resumes || 0 }}</div>
              <div class="stat-lbl">Resumes Analyzed</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-rose-50 text-rose-600">⚡</div>
            <div>
              <div class="stat-val">{{ adminData?.stats?.avg_match_score || 0 }}%</div>
              <div class="stat-lbl">Avg Match Rate</div>
            </div>
          </div>
        </div>

        <!-- 2 Column Overview Table -->
        <div class="grid grid-cols-2 gap-8">
          <!-- Recent Users -->
          <div class="card p-6 overflow-hidden">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-bold text-slate-900 text-base">Recent Platform Registrations</h3>
              <router-link to="/admin/users" class="text-xs text-indigo-600 font-semibold hover:underline">
                Manage All →
              </router-link>
            </div>

            <div class="table-responsive">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="border-b border-slate-100 text-slate-400">
                    <th class="py-2">User</th>
                    <th class="py-2">Role</th>
                    <th class="py-2">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="u in adminData?.recent_users" :key="u.id" class="py-2">
                    <td class="py-2 font-semibold text-slate-800">{{ u.name }} ({{ u.email }})</td>
                    <td class="py-2"><span class="badge" :class="'badge-' + (u.role === 'company' ? 'success' : 'primary')">{{ u.role }}</span></td>
                    <td class="py-2"><span class="badge badge-success">{{ u.status }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Recent Applications -->
          <div class="card p-6 overflow-hidden">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-bold text-slate-900 text-base">Platform Job Applications</h3>
              <router-link to="/admin/applications" class="text-xs text-indigo-600 font-semibold hover:underline">
                View All →
              </router-link>
            </div>

            <div class="table-responsive">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="border-b border-slate-100 text-slate-400">
                    <th class="py-2">Candidate & Job</th>
                    <th class="py-2">AI Match</th>
                    <th class="py-2">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="a in adminData?.recent_applications" :key="a.id">
                    <td class="py-2 font-semibold text-slate-800">
                      {{ a.candidate_name }} → {{ a.job_title }}
                    </td>
                    <td class="py-2"><MatchScoreBadge :score="a.match_score" size="sm" /></td>
                    <td class="py-2"><span class="badge badge-primary">{{ a.status }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </template>
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
const adminData = ref(null)
const loading = ref(true)

const fetchDashboard = async () => {
  loading.value = true
  try {
    const res = await adminApi.getDashboard()
    if (res.success) {
      adminData.value = res.data
    }
  } catch (err) {
    toastStore.error('Failed to load admin dashboard')
  } finally {
    loading.value = false
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
  color: #92400e;
  background: #fef3c7;
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
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}
.stat-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-radius: 16px;
}
.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}
.stat-val {
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.1;
}
.stat-lbl {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
}
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>
