<template>
  <div class="student-dashboard py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <!-- Top Welcome Banner -->
      <div class="welcome-banner card card-glass p-8 mb-8">
        <div class="welcome-content">
          <div class="welcome-badge">👨‍🎓 Student Portal</div>
          <h1 class="welcome-title">Welcome back, {{ authStore.userName }}!</h1>
          <p class="welcome-subtitle">
            {{ dashboardData?.resume ? 'Your resume is analyzed and actively matched against open tech roles.' : 'Upload your resume to discover your extracted skills and receive personalized AI job recommendations.' }}
          </p>
        </div>
        <div class="welcome-action">
          <router-link to="/student/resume" class="btn btn-primary">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            {{ dashboardData?.resume ? 'View Resume Health' : 'Upload Resume Now' }}
          </router-link>
        </div>
      </div>

      <!-- Loading State -->
      <Loader v-if="loading" text="Loading dashboard metrics & AI recommendations..." />

      <template v-else>
        <!-- Quick Stats Row -->
        <div class="stats-grid mb-8">
          <div class="stat-card card p-6">
            <div class="stat-icon bg-indigo-50 text-indigo-600">📄</div>
            <div>
              <div class="stat-val">{{ dashboardData?.stats?.total_applied || 0 }}</div>
              <div class="stat-lbl">Jobs Applied</div>
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
            <div class="stat-icon bg-purple-50 text-purple-600">🎯</div>
            <div>
              <div class="stat-val">{{ dashboardData?.stats?.interview || 0 }}</div>
              <div class="stat-lbl">Interviews</div>
            </div>
          </div>

          <div class="stat-card card p-6">
            <div class="stat-icon bg-amber-50 text-amber-600">★</div>
            <div>
              <div class="stat-val">{{ dashboardData?.stats?.saved_jobs || 0 }}</div>
              <div class="stat-lbl">Saved Jobs</div>
            </div>
          </div>
        </div>

        <!-- Two Column Main Layout -->
        <div class="dashboard-main-grid mb-8">
          <!-- Left: Resume Health & Skills Matrix -->
          <div class="dashboard-col">
            <!-- Resume Health Score Card -->
            <div class="card p-6 mb-6">
              <div class="card-header-row mb-4">
                <h3 class="text-lg font-bold text-slate-900">ATS Resume Health</h3>
                <router-link to="/student/resume" class="text-sm text-indigo-600 font-semibold hover:underline">
                  Full Audit →
                </router-link>
              </div>

              <div v-if="dashboardData?.resume" class="score-display-box">
                <div class="score-circle" :class="getScoreColorClass(dashboardData.resume_score)">
                  <span class="score-number">{{ dashboardData.resume_score }}</span>
                  <span class="score-out">/100</span>
                </div>
                <div class="score-feedback">
                  <div class="font-bold text-slate-800 text-base mb-1">
                    {{ getScoreLabel(dashboardData.resume_score) }}
                  </div>
                  <p class="text-sm text-slate-600">
                    File: <strong class="text-slate-700">{{ dashboardData.resume.file_name }}</strong>
                  </p>
                  <p class="text-xs text-slate-500 mt-1">
                    Uploaded on {{ formatDate(dashboardData.resume.created_at) }}
                  </p>
                </div>
              </div>

              <div v-else class="empty-resume-box text-center p-6 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                <p class="text-sm text-slate-600 mb-3">No resume uploaded yet. Upload to see your score.</p>
                <router-link to="/student/resume" class="btn btn-primary btn-sm">Upload Resume</router-link>
              </div>
            </div>

            <!-- Extracted Skills Matrix Card -->
            <div class="card p-6">
              <div class="card-header-row mb-4">
                <h3 class="text-lg font-bold text-slate-900">Detected Skills ({{ dashboardData?.skills_count || 0 }})</h3>
                <router-link to="/student/skills" class="text-sm text-indigo-600 font-semibold hover:underline">
                  Manage Skills →
                </router-link>
              </div>

              <div v-if="dashboardData?.skills && dashboardData.skills.length > 0" class="skills-wrap">
                <span
                  v-for="s in dashboardData.skills.slice(0, 12)"
                  :key="s.skill_name"
                  class="badge badge-primary text-xs"
                >
                  {{ s.skill_name }}
                </span>
              </div>
              <p v-else class="text-sm text-slate-500">Skills will appear here once your resume is analyzed.</p>
            </div>
          </div>

          <!-- Right: Top AI Job Matches -->
          <div class="dashboard-col">
            <div class="card p-6">
              <div class="card-header-row mb-4">
                <div>
                  <h3 class="text-lg font-bold text-slate-900">Top AI Job Recommendations</h3>
                  <p class="text-xs text-slate-500">Ranked by algorithm compatibility with your resume</p>
                </div>
                <router-link to="/jobs" class="text-sm text-indigo-600 font-semibold hover:underline">
                  Browse All (6+) →
                </router-link>
              </div>

              <div v-if="dashboardData?.recommended_jobs && dashboardData.recommended_jobs.length > 0" class="recs-list">
                <div
                  v-for="job in dashboardData.recommended_jobs"
                  :key="job.id"
                  class="rec-job-item p-4 rounded-xl border border-slate-200 hover:border-indigo-300 transition"
                >
                  <div class="rec-top flex justify-between items-start mb-2">
                    <div>
                      <router-link :to="`/jobs/${job.id}`" class="font-bold text-slate-900 hover:text-indigo-600 text-base">
                        {{ job.title }}
                      </router-link>
                      <div class="text-xs text-slate-500">{{ job.company_name }} • {{ job.location }}</div>
                    </div>
                    <MatchScoreBadge :score="job.match_score" size="sm" />
                  </div>

                  <div v-if="job.why_matched" class="ai-why-matched text-xs text-indigo-900 bg-indigo-50 p-2 rounded-lg mb-3">
                    ✨ {{ job.why_matched }}
                  </div>

                  <div class="rec-bottom flex items-center justify-between">
                    <span class="text-xs text-slate-500 font-medium">
                      {{ job.job_type }} • ${{ Number(job.salary_min || 70000).toLocaleString() }}/yr
                    </span>
                    <router-link :to="`/jobs/${job.id}`" class="btn btn-secondary btn-sm text-xs">
                      View Role
                    </router-link>
                  </div>
                </div>
              </div>

              <div v-else class="text-center p-8 text-slate-500">
                No recommendations found. Browse the job board to explore positions!
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { studentApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import MatchScoreBadge from '@/components/common/MatchScoreBadge.vue'
import Loader from '@/components/common/Loader.vue'

const authStore = useAuthStore()
const dashboardData = ref(null)
const loading = ref(true)

const fetchDashboard = async () => {
  loading.value = true
  try {
    const res = await studentApi.getDashboard()
    if (res.success) {
      dashboardData.value = res.data
    }
  } catch (err) {
    console.error('Failed to load student dashboard:', err)
  } finally {
    loading.value = false
  }
}

const getScoreColorClass = (score) => {
  if (score >= 80) return 'score-excellent'
  if (score >= 65) return 'score-good'
  return 'score-needs-work'
}

const getScoreLabel = (score) => {
  if (score >= 85) return '🔥 Outstanding ATS Compatibility'
  if (score >= 70) return '👍 Strong Resume Health'
  if (score >= 50) return '⚠️ Moderate - Action Items Available'
  return '🚨 Needs Improvement'
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
  fetchDashboard()
})
</script>

<style scoped>
.welcome-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 20px;
}

.welcome-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #4f46e5;
  background: #eef2ff;
  padding: 3px 10px;
  border-radius: 999px;
  margin-bottom: 8px;
}

.welcome-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 6px;
}

.welcome-subtitle {
  font-size: 0.95rem;
  color: #475569;
  max-width: 600px;
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

.dashboard-main-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
}

.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.score-display-box {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
}

.score-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 800;
}

.score-excellent {
  background: #ecfdf5;
  color: #047857;
  border: 3px solid #10b981;
}
.score-good {
  background: #eff6ff;
  color: #1d4ed8;
  border: 3px solid #3b82f6;
}
.score-needs-work {
  background: #fffbeb;
  color: #b45309;
  border: 3px solid #f59e0b;
}

.score-number {
  font-size: 1.5rem;
  line-height: 1;
}
.score-out {
  font-size: 0.65rem;
  color: #64748b;
}

.skills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.recs-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rec-job-item {
  background: #ffffff;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .dashboard-main-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 640px) {
  .welcome-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
