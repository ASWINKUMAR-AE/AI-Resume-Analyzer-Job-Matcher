<template>
  <div class="jobs-page bg-slate-50 min-h-screen py-10">
    <div class="container">
      <!-- Search & Filter Header -->
      <div class="jobs-header-card card p-6 mb-8">
        <div class="header-top mb-4">
          <h1 class="text-2xl font-bold text-slate-900">Explore Tech Positions</h1>
          <p class="text-slate-600 text-sm">
            <span v-if="authStore.isStudent">🎯 Showing personalized AI match scores calculated from your resume.</span>
            <span v-else>💡 Sign in as a student to unlock real-time AI resume matching for every job.</span>
          </p>
        </div>

        <!-- Search & Filter Controls -->
        <div class="filters-row">
          <div class="search-input-group flex-1">
            <input
              v-model="searchQuery"
              type="text"
              class="form-input"
              placeholder="Search by title, skills (e.g. Python, Vue), company..."
              @keyup.enter="fetchJobs"
            />
          </div>

          <div class="filter-group">
            <select v-model="selectedJobType" class="form-select" @change="fetchJobs">
              <option value="all">All Job Types</option>
              <option value="Full Time">Full Time</option>
              <option value="Part Time">Part Time</option>
              <option value="Internship">Internship</option>
              <option value="Contract">Contract</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
            </select>
          </div>

          <div class="filter-group">
            <input
              v-model="selectedLocation"
              type="text"
              class="form-input"
              placeholder="Location..."
              @keyup.enter="fetchJobs"
            />
          </div>

          <div class="filter-group" v-if="authStore.isStudent">
            <select v-model="sortBy" class="form-select" @change="fetchJobs">
              <option value="newest">Sort: Newest First</option>
              <option value="match">Sort: Highest Match %</option>
            </select>
          </div>

          <button class="btn btn-primary" @click="fetchJobs">
            Search
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <Loader v-if="loading" text="Loading active jobs & AI matching scores..." />

      <!-- Error State -->
      <div v-else-if="error" class="card p-6 text-center text-rose-600">
        <p>{{ error }}</p>
        <button class="btn btn-secondary btn-sm mt-4" @click="fetchJobs">Retry</button>
      </div>

      <!-- Empty State -->
      <EmptyState
        v-else-if="jobs.length === 0"
        title="No Matching Jobs Found"
        message="Try adjusting your keyword search or location filters."
        icon="🔍"
      >
        <template #action>
          <button class="btn btn-secondary btn-sm" @click="resetFilters">Clear Filters</button>
        </template>
      </EmptyState>

      <!-- Jobs Grid -->
      <div v-else class="jobs-grid">
        <div v-for="job in jobs" :key="job.id" class="job-card card card-interactive">
          <!-- Card Top -->
          <div class="job-card-header">
            <div class="company-badge-group">
              <div class="company-avatar">
                {{ (job.company_name || 'C').charAt(0).toUpperCase() }}
              </div>
              <div>
                <h3 class="job-title">{{ job.title }}</h3>
                <span class="company-name">{{ job.company_name }}</span>
              </div>
            </div>

            <!-- Match Score Badge if computed -->
            <MatchScoreBadge
              v-if="job.match_score !== null && job.match_score !== undefined"
              :score="job.match_score"
              size="md"
            />
          </div>

          <!-- Job Details Badges -->
          <div class="job-meta-row">
            <span class="meta-item">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              {{ job.location || 'Remote' }}
            </span>
            <span class="meta-item">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
              </svg>
              {{ job.job_type }}
            </span>
            <span class="meta-item">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              {{ job.experience_required || '1+ years' }}
            </span>
            <span v-if="job.salary_min" class="meta-item text-emerald-600 font-semibold">
              ${{ Number(job.salary_min).toLocaleString() }} - ${{ Number(job.salary_max || job.salary_min).toLocaleString() }}
            </span>
          </div>

          <!-- Description Preview -->
          <p class="job-desc-preview">{{ truncateText(job.description, 160) }}</p>

          <!-- Skills Chips -->
          <div class="job-skills-container">
            <span
              v-for="skill in getSkillList(job.skills)"
              :key="skill"
              class="badge"
              :class="isSkillMatched(job, skill) ? 'badge-success' : 'badge-primary'"
            >
              {{ isSkillMatched(job, skill) ? '✓ ' : '' }}{{ skill }}
            </span>
          </div>

          <!-- AI Why Matched Insight -->
          <div v-if="job.why_matched" class="ai-job-insight">
            <span class="ai-sparkle-sm">✨</span>
            <span class="ai-insight-text">{{ job.why_matched }}</span>
          </div>

          <!-- Card Actions -->
          <div class="job-card-actions">
            <router-link :to="`/jobs/${job.id}`" class="btn btn-secondary btn-sm">
              View Details
            </router-link>

            <div class="right-actions">
              <!-- Bookmark Button for Students -->
              <button
                v-if="authStore.isStudent"
                class="btn btn-sm"
                :class="job.is_saved ? 'btn-primary' : 'btn-secondary'"
                @click="toggleSave(job)"
                title="Save Job"
              >
                {{ job.is_saved ? '★ Saved' : '☆ Save' }}
              </button>

              <!-- Apply Button -->
              <button
                v-if="authStore.isStudent"
                class="btn btn-primary btn-sm"
                :disabled="job.applied_status"
                @click="openApplyModal(job)"
              >
                {{ job.applied_status ? 'Applied (' + job.applied_status + ')' : 'Apply Now' }}
              </button>

              <router-link v-else-if="!authStore.isAuthenticated" to="/login" class="btn btn-primary btn-sm">
                Sign in to Apply
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Apply Modal Dialog -->
    <Modal
      :is-open="applyModalOpen"
      :title="`Apply for: ${selectedJob?.title}`"
      max-width="md"
      @close="applyModalOpen = false"
    >
      <div v-if="selectedJob" class="apply-modal-content">
        <div class="company-sub mb-4">
          <strong>{{ selectedJob.company_name }}</strong> • {{ selectedJob.location }}
        </div>

        <div v-if="selectedJob.match_score" class="p-3 bg-indigo-50 border border-indigo-100 rounded-lg mb-4 flex items-center justify-between">
          <span class="text-sm font-semibold text-indigo-900">Your AI Resume Match:</span>
          <MatchScoreBadge :score="selectedJob.match_score" size="sm" />
        </div>

        <div class="form-group">
          <label class="form-label">Cover Note / Brief Message to Employer (Optional)</label>
          <textarea
            v-model="applyCoverNote"
            class="form-textarea"
            rows="4"
            placeholder="Introduce yourself and highlight key projects or relevant skills for this position..."
          ></textarea>
        </div>
      </div>

      <template #footer>
        <button class="btn btn-secondary btn-sm" @click="applyModalOpen = false">Cancel</button>
        <button class="btn btn-primary btn-sm" :disabled="submittingApply" @click="submitApplication">
          {{ submittingApply ? 'Submitting...' : 'Confirm & Submit Application' }}
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { jobsApi, studentApi, applicationsApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import MatchScoreBadge from '@/components/common/MatchScoreBadge.vue'
import Loader from '@/components/common/Loader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import Modal from '@/components/common/Modal.vue'

const authStore = useAuthStore()
const toastStore = useToastStore()

const jobs = ref([])
const loading = ref(true)
const error = ref(null)

const searchQuery = ref('')
const selectedJobType = ref('all')
const selectedLocation = ref('')
const sortBy = ref('newest')

// Apply Modal
const applyModalOpen = ref(false)
const selectedJob = ref(null)
const applyCoverNote = ref('')
const submittingApply = ref(false)

const fetchJobs = async () => {
  loading.value = true
  error.value = null
  try {
    const params = {
      q: searchQuery.value,
      job_type: selectedJobType.value,
      location: selectedLocation.value,
      sort: sortBy.value
    }
    const res = await jobsApi.getJobs(params)
    if (res.success) {
      jobs.value = res.data || []
    }
  } catch (err) {
    error.value = err.message || 'Failed to load jobs'
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedJobType.value = 'all'
  selectedLocation.value = ''
  sortBy.value = 'newest'
  fetchJobs()
}

const getSkillList = (skillsStr) => {
  if (!skillsStr) return []
  return skillsStr.split(',').map((s) => s.trim()).filter(Boolean).slice(0, 6)
}

const isSkillMatched = (job, skill) => {
  if (!job.matched_skills || !Array.isArray(job.matched_skills)) return false
  return job.matched_skills.some((ms) => ms.toLowerCase() === skill.toLowerCase())
}

const truncateText = (text, len = 140) => {
  if (!text) return ''
  return text.length > len ? text.substring(0, len) + '...' : text
}

const toggleSave = async (job) => {
  try {
    const res = await studentApi.toggleSaveJob(job.id)
    if (res.success) {
      job.is_saved = res.data.is_saved
      toastStore.success(res.message)
    }
  } catch (err) {
    toastStore.error(err.message)
  }
}

const openApplyModal = (job) => {
  selectedJob.value = job
  applyCoverNote.value = ''
  applyModalOpen.value = true
}

const submitApplication = async () => {
  if (!selectedJob.value) return
  submittingApply.value = true
  try {
    const res = await applicationsApi.applyForJob(selectedJob.value.id, {
      cover_note: applyCoverNote.value
    })
    if (res.success) {
      toastStore.success('Application submitted successfully!')
      selectedJob.value.applied_status = 'Applied'
      applyModalOpen.value = false
    }
  } catch (err) {
    toastStore.error(err.message)
  } finally {
    submittingApply.value = false
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.jobs-header-card {
  border-radius: 16px;
}

.filters-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-group select, .filter-group input {
  min-width: 170px;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.job-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
}

.job-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.company-badge-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.company-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
  color: white;
  font-weight: 800;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.job-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.25;
}

.company-name {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.job-meta-row {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  font-size: 0.825rem;
  color: #475569;
  margin-bottom: 12px;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.job-desc-preview {
  font-size: 0.9rem;
  color: #475569;
  line-height: 1.5;
  margin-bottom: 16px;
  flex: 1;
}

.job-skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.ai-job-insight {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  background: #f5f3ff;
  border: 1px solid #ede9fe;
  border-radius: 10px;
  padding: 8px 12px;
  margin-bottom: 16px;
}

.ai-sparkle-sm {
  font-size: 14px;
}

.ai-insight-text {
  font-size: 0.8rem;
  color: #5b21b6;
  font-weight: 500;
  line-height: 1.35;
}

.job-card-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #f1f5f9;
  padding-top: 16px;
  margin-top: auto;
}

.right-actions {
  display: flex;
  gap: 8px;
}

@media (max-width: 960px) {
  .jobs-grid {
    grid-template-columns: 1fr;
  }
}
</style>
