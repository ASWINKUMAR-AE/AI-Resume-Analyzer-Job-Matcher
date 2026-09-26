<template>
  <div class="job-detail-page py-8 bg-slate-50 min-h-screen">
    <div class="container max-w-5xl">
      <!-- Back Link -->
      <div class="mb-4">
        <router-link to="/jobs" class="inline-flex items-center gap-1 text-sm font-semibold text-indigo-600 hover:underline">
          ← Back to All Jobs
        </router-link>
      </div>

      <Loader v-if="loading" text="Loading job details & AI compatibility..." />

      <div v-else-if="error" class="card p-6 text-center text-rose-600">
        <p>{{ error }}</p>
        <router-link to="/jobs" class="btn btn-secondary btn-sm mt-4">Return to Jobs</router-link>
      </div>

      <div v-else-if="job" class="job-content-grid">
        <!-- Main Column -->
        <div class="main-column flex flex-col gap-6">
          <!-- Job Header Card -->
          <div class="card p-8">
            <div class="flex items-start justify-between flex-wrap gap-4 mb-4">
              <div>
                <h1 class="text-2xl font-bold text-slate-900 mb-1">{{ job.title }}</h1>
                <div class="flex items-center gap-2 text-slate-600 text-sm font-medium">
                  <span class="text-slate-800 font-bold">{{ job.company_name }}</span>
                  <span>•</span>
                  <span>{{ job.location }}</span>
                  <span>•</span>
                  <span class="badge badge-primary">{{ job.job_type }}</span>
                </div>
              </div>

              <!-- Top Match Pill if available -->
              <MatchScoreBadge
                v-if="job.ai_evaluation?.match_score"
                :score="job.ai_evaluation.match_score"
                size="lg"
              />
            </div>

            <!-- Meta attributes -->
            <div class="grid grid-cols-3 gap-4 p-4 bg-slate-50 rounded-xl border border-slate-200 text-sm mb-6">
              <div>
                <span class="text-slate-500 block text-xs">Experience</span>
                <strong class="text-slate-800">{{ job.experience_required || '1-3 years' }}</strong>
              </div>
              <div>
                <span class="text-slate-500 block text-xs">Salary Range</span>
                <strong class="text-emerald-700">
                  ${{ Number(job.salary_min || 75000).toLocaleString() }} - ${{ Number(job.salary_max || 110000).toLocaleString() }}
                </strong>
              </div>
              <div>
                <span class="text-slate-500 block text-xs">Deadline</span>
                <strong class="text-slate-800">{{ formatDate(job.application_deadline) || 'Open Until Filled' }}</strong>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-3">
              <button
                v-if="authStore.isStudent"
                class="btn btn-primary"
                :disabled="job.applied_status"
                @click="openApplyModal"
              >
                {{ job.applied_status ? `Applied (${job.applied_status})` : 'Apply for this Role' }}
              </button>
              <router-link v-else-if="!authStore.isAuthenticated" to="/login" class="btn btn-primary">
                Sign in to Apply
              </router-link>

              <button
                v-if="authStore.isStudent"
                class="btn btn-secondary"
                @click="toggleSave"
              >
                {{ job.is_saved ? '★ Saved' : '☆ Save Job' }}
              </button>

              <router-link
                v-if="authStore.isStudent"
                :to="`/student/assistant?job_id=${job.id}`"
                class="btn btn-outline-primary"
              >
                ✨ Ask AI Coach
              </router-link>
            </div>
          </div>

          <!-- AI Compatibility Breakdown Card (if candidate has uploaded resume) -->
          <div v-if="job.ai_evaluation" class="card p-8 border-indigo-200 shadow-md">
            <div class="flex items-center justify-between mb-6 pb-4 border-b border-slate-100">
              <div>
                <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2">
                  <span class="text-indigo-600">⚡</span> AI Compatibility Analysis
                </h2>
                <p class="text-xs text-slate-500 mt-1">Explainable multi-factor scoring breakdown</p>
              </div>
              <MatchScoreBadge :score="job.ai_evaluation.match_score" size="md" />
            </div>

            <!-- Score Progress Bars -->
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>Skill Overlap (45% wt)</span>
                  <span>{{ Math.round(job.ai_evaluation.score_breakdown?.skill_match || 0) }}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" :style="{ width: (job.ai_evaluation.score_breakdown?.skill_match || 0) + '%' }"></div></div>
              </div>

              <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>TF-IDF Text Similarity (30% wt)</span>
                  <span>{{ Math.round(job.ai_evaluation.score_breakdown?.text_similarity || 0) }}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" :style="{ width: (job.ai_evaluation.score_breakdown?.text_similarity || 0) + '%' }"></div></div>
              </div>

              <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>Experience Match (15% wt)</span>
                  <span>{{ Math.round(job.ai_evaluation.score_breakdown?.experience_match || 0) }}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" :style="{ width: (job.ai_evaluation.score_breakdown?.experience_match || 0) + '%' }"></div></div>
              </div>

              <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>Education Match (10% wt)</span>
                  <span>{{ Math.round(job.ai_evaluation.score_breakdown?.education_match || 0) }}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" :style="{ width: (job.ai_evaluation.score_breakdown?.education_match || 0) + '%' }"></div></div>
              </div>
            </div>

            <!-- Matched vs Missing Skills -->
            <div class="grid grid-cols-2 gap-6">
              <div>
                <h4 class="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-2">
                  ✓ Matched Skills ({{ job.ai_evaluation.matched_skills?.length || 0 }})
                </h4>
                <div class="flex flex-wrap gap-1.5">
                  <span
                    v-for="s in job.ai_evaluation.matched_skills"
                    :key="s"
                    class="badge badge-success text-xs"
                  >
                    ✓ {{ s }}
                  </span>
                </div>
              </div>

              <div>
                <h4 class="text-xs font-bold text-rose-800 uppercase tracking-wider mb-2">
                  • Skills Gap ({{ job.ai_evaluation.missing_skills?.length || 0 }})
                </h4>
                <div class="flex flex-wrap gap-1.5">
                  <span
                    v-for="s in job.ai_evaluation.missing_skills"
                    :key="s"
                    class="badge badge-danger text-xs"
                  >
                    {{ s }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Description Section -->
          <div class="card p-8">
            <h3 class="text-lg font-bold text-slate-900 mb-4">Job Description</h3>
            <div class="prose text-slate-700 leading-relaxed text-sm whitespace-pre-line">
              {{ job.description }}
            </div>

            <h3 v-if="job.requirements" class="text-lg font-bold text-slate-900 mt-8 mb-4">Requirements & Qualifications</h3>
            <div v-if="job.requirements" class="prose text-slate-700 leading-relaxed text-sm whitespace-pre-line">
              {{ job.requirements }}
            </div>

            <h3 class="text-lg font-bold text-slate-900 mt-8 mb-4">Target Skills</h3>
            <div class="flex flex-wrap gap-2">
              <span v-for="sk in (job.skills || '').split(',')" :key="sk" class="badge badge-primary py-1 px-3">
                {{ sk.trim() }}
              </span>
            </div>
          </div>
        </div>

        <!-- Sidebar Column: Company Profile -->
        <div class="sidebar-column flex flex-col gap-6">
          <div class="card p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="company-avatar">
                {{ (job.company_name || 'C').charAt(0).toUpperCase() }}
              </div>
              <div>
                <h3 class="font-bold text-slate-900 text-base">{{ job.company_name }}</h3>
                <span class="text-xs text-slate-500">{{ job.industry || 'Technology' }}</span>
              </div>
            </div>

            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              {{ job.company_description || 'Innovative technology company building next-generation products.' }}
            </p>

            <div class="text-xs text-slate-500 flex flex-col gap-2 pt-3 border-t border-slate-100">
              <div>📍 <strong>Location:</strong> {{ job.company_location || job.location }}</div>
              <div v-if="job.website">
                🌐 <strong>Website:</strong> <a :href="job.website" target="_blank" class="text-indigo-600 hover:underline">{{ job.website }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Apply Modal -->
    <Modal
      :is-open="applyModalOpen"
      :title="`Apply for: ${job?.title}`"
      max-width="md"
      @close="applyModalOpen = false"
    >
      <div v-if="job" class="apply-modal-content">
        <div class="p-3 bg-indigo-50 border border-indigo-100 rounded-lg mb-4 flex items-center justify-between">
          <span class="text-sm font-semibold text-indigo-900">Your AI Compatibility:</span>
          <MatchScoreBadge :score="job.ai_evaluation?.match_score || 75" size="sm" />
        </div>

        <div class="form-group">
          <label class="form-label">Cover Note to Hiring Team (Optional)</label>
          <textarea
            v-model="applyCoverNote"
            class="form-textarea"
            rows="4"
            placeholder="Briefly describe why you are a great match for this position..."
          ></textarea>
        </div>
      </div>

      <template #footer>
        <button class="btn btn-secondary btn-sm" @click="applyModalOpen = false">Cancel</button>
        <button class="btn btn-primary btn-sm" :disabled="submitting" @click="submitApplication">
          {{ submitting ? 'Submitting...' : 'Confirm & Apply' }}
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { jobsApi, studentApi, applicationsApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import MatchScoreBadge from '@/components/common/MatchScoreBadge.vue'
import Loader from '@/components/common/Loader.vue'
import Modal from '@/components/common/Modal.vue'

const route = useRoute()
const authStore = useAuthStore()
const toastStore = useToastStore()

const job = ref(null)
const loading = ref(true)
const error = ref(null)

const applyModalOpen = ref(false)
const applyCoverNote = ref('')
const submitting = ref(false)

const fetchJob = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await jobsApi.getJobDetail(route.params.id)
    if (res.success && res.data) {
      job.value = res.data
    } else {
      error.value = 'Job listing not found.'
    }
  } catch (err) {
    error.value = err.message || 'Failed to load job details.'
  } finally {
    loading.value = false
  }
}

const toggleSave = async () => {
  if (!job.value) return
  try {
    const res = await studentApi.toggleSaveJob(job.value.id)
    if (res.success) {
      job.value.is_saved = res.data.is_saved
      toastStore.success(res.message)
    }
  } catch (err) {
    toastStore.error(err.message)
  }
}

const openApplyModal = () => {
  applyCoverNote.value = ''
  applyModalOpen.value = true
}

const submitApplication = async () => {
  submitting.value = true
  try {
    const res = await applicationsApi.applyForJob(job.value.id, {
      cover_note: applyCoverNote.value
    })
    if (res.success) {
      toastStore.success('Application submitted successfully!')
      job.value.applied_status = 'Applied'
      applyModalOpen.value = false
    }
  } catch (err) {
    toastStore.error(err.message)
  } finally {
    submitting.value = false
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
  fetchJob()
})
</script>

<style scoped>
.job-content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
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

@media (max-width: 960px) {
  .job-content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
