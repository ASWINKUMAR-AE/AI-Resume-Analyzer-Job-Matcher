<template>
  <div class="applicants-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <!-- Header & Filters -->
      <div class="header-card card p-6 mb-8">
        <div class="flex items-center justify-between flex-wrap gap-4 mb-4">
          <div>
            <h1 class="text-2xl font-bold text-slate-900">AI-Ranked Applicant Management</h1>
            <p class="text-slate-600 text-sm mt-1">Review candidates ranked by algorithm compatibility score with full skill breakdowns.</p>
          </div>
          <div class="badge badge-primary py-1 px-3">
            {{ applicants.length }} Candidates Found
          </div>
        </div>

        <div class="filters-row flex flex-wrap gap-3">
          <div class="flex-1 min-w-[200px]">
            <input
              v-model="searchQuery"
              type="text"
              class="form-input"
              placeholder="Search candidate name, email, or degree..."
              @input="filterApplicants"
            />
          </div>

          <div class="w-48">
            <select v-model="selectedStatus" class="form-select" @change="fetchApplicants">
              <option value="all">All Statuses</option>
              <option value="Applied">Applied</option>
              <option value="Under Review">Under Review</option>
              <option value="Shortlisted">Shortlisted</option>
              <option value="Interview">Interview</option>
              <option value="Selected">Selected</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>
        </div>
      </div>

      <Loader v-if="loading" text="Loading ranked applicants..." />

      <EmptyState
        v-else-if="filteredApplicants.length === 0"
        title="No Applicants Found"
        message="No candidates match your current filter criteria."
        icon="👥"
      />

      <!-- Applicants List Table -->
      <div v-else class="card overflow-hidden">
        <div class="table-responsive">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
                <th class="p-4">Candidate & Contact</th>
                <th class="p-4">Applied Job</th>
                <th class="p-4">AI Match</th>
                <th class="p-4">Resume Score</th>
                <th class="p-4">Hiring Status</th>
                <th class="p-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-sm">
              <tr v-for="app in filteredApplicants" :key="app.id" class="hover:bg-slate-50/80 transition">
                <!-- Candidate Info -->
                <td class="p-4">
                  <div class="font-bold text-slate-900">{{ app.candidate_name }}</div>
                  <div class="text-xs text-slate-500">{{ app.candidate_email }} • {{ app.candidate_phone || 'No phone' }}</div>
                  <div class="text-xs text-slate-600 mt-1">
                    🎓 {{ app.college || 'University' }} ({{ app.degree || 'Degree' }})
                  </div>
                </td>

                <!-- Applied Job -->
                <td class="p-4 font-semibold text-slate-800">
                  {{ app.job_title }}
                  <span class="block text-xs font-normal text-slate-500">{{ app.job_type }}</span>
                </td>

                <!-- AI Match -->
                <td class="p-4">
                  <MatchScoreBadge :score="app.match_score" size="sm" />
                </td>

                <!-- Resume Score -->
                <td class="p-4 text-xs font-bold text-slate-700">
                  {{ app.resume_score || 0 }}/100
                </td>

                <!-- Hiring Status Dropdown -->
                <td class="p-4">
                  <select
                    v-model="app.status"
                    class="form-select text-xs py-1 px-2.5 w-36 font-semibold"
                    :class="getStatusSelectClass(app.status)"
                    @change="handleStatusChange(app.id, app.status)"
                  >
                    <option value="Applied">Applied</option>
                    <option value="Under Review">Under Review</option>
                    <option value="Shortlisted">⭐ Shortlisted</option>
                    <option value="Interview">🎯 Interview</option>
                    <option value="Selected">🎉 Selected</option>
                    <option value="Rejected">✕ Rejected</option>
                  </select>
                </td>

                <!-- Actions -->
                <td class="p-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button class="btn btn-secondary btn-sm text-xs" @click="viewCandidateDetail(app)">
                      Inspect AI
                    </button>
                    <a
                      :href="`/api/resume/download/${app.resume_id}`"
                      class="btn btn-outline-primary btn-sm text-xs"
                      target="_blank"
                      download
                    >
                      Resume 📥
                    </a>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Candidate Detail Modal -->
    <Modal
      :is-open="detailModalOpen"
      :title="`Applicant AI Breakdown: ${selectedCandidate?.candidate_name}`"
      max-width="lg"
      @close="detailModalOpen = false"
    >
      <div v-if="selectedCandidate" class="candidate-detail-modal-body">
        <div class="flex items-center justify-between p-4 bg-indigo-50 border border-indigo-100 rounded-xl mb-4">
          <div>
            <h3 class="font-bold text-indigo-950 text-base">{{ selectedCandidate.candidate_name }}</h3>
            <span class="text-xs text-indigo-700">{{ selectedCandidate.candidate_email }} • {{ selectedCandidate.degree }}</span>
          </div>
          <MatchScoreBadge :score="selectedCandidate.match_score" size="md" />
        </div>

        <div v-if="selectedCandidate.cover_note" class="mb-4 p-3 bg-slate-50 border rounded-lg">
          <strong class="text-xs font-bold text-slate-700 block mb-1">Cover Note:</strong>
          <p class="text-xs text-slate-600 italic">{{ selectedCandidate.cover_note }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-4">
          <div class="p-3 bg-slate-50 border rounded-lg">
            <span class="text-xs text-slate-500 block">Experience Level</span>
            <strong class="text-sm text-slate-800">{{ selectedCandidate.experience || '1-2 years' }}</strong>
          </div>
          <div class="p-3 bg-slate-50 border rounded-lg">
            <span class="text-xs text-slate-500 block">Resume Health Score</span>
            <strong class="text-sm text-emerald-700">{{ selectedCandidate.resume_score || 0 }}/100</strong>
          </div>
        </div>

        <div class="links-row flex gap-3 text-xs text-indigo-600 font-medium mb-4">
          <a v-if="selectedCandidate.linkedin_url" :href="selectedCandidate.linkedin_url" target="_blank" class="hover:underline">
            🔗 LinkedIn Profile
          </a>
          <a v-if="selectedCandidate.github_url" :href="selectedCandidate.github_url" target="_blank" class="hover:underline">
            🐙 GitHub Profile
          </a>
        </div>
      </div>

      <template #footer>
        <button class="btn btn-secondary btn-sm" @click="detailModalOpen = false">Close</button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { applicationsApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import MatchScoreBadge from '@/components/common/MatchScoreBadge.vue'
import Loader from '@/components/common/Loader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import Modal from '@/components/common/Modal.vue'

const route = useRoute()
const toastStore = useToastStore()

const applicants = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedStatus = ref('all')
const targetJobId = ref(route.query.job_id || null)

// Detail modal
const detailModalOpen = ref(false)
const selectedCandidate = ref(null)

const fetchApplicants = async () => {
  loading.value = true
  try {
    const params = {
      job_id: targetJobId.value,
      status: selectedStatus.value !== 'all' ? selectedStatus.value : undefined
    }
    const res = await applicationsApi.getCompanyApplications(params)
    if (res.success) {
      applicants.value = res.data || []
    }
  } catch (err) {
    toastStore.error('Failed to load applicants')
  } finally {
    loading.value = false
  }
}

const filteredApplicants = computed(() => {
  if (!searchQuery.value.trim()) return applicants.value
  const q = searchQuery.value.toLowerCase()
  return applicants.value.filter((a) =>
    (a.candidate_name || '').toLowerCase().includes(q) ||
    (a.candidate_email || '').toLowerCase().includes(q) ||
    (a.job_title || '').toLowerCase().includes(q)
  )
})

const handleStatusChange = async (appId, newStatus) => {
  try {
    const res = await applicationsApi.updateStatus(appId, newStatus)
    if (res.success) {
      toastStore.success(`Candidate status updated to '${newStatus}'!`)
    }
  } catch (err) {
    toastStore.error(err.message)
  }
}

const viewCandidateDetail = (candidate) => {
  selectedCandidate.value = candidate
  detailModalOpen.value = true
}

const getStatusSelectClass = (status) => {
  if (status === 'Shortlisted') return 'bg-emerald-50 text-emerald-800 border-emerald-300'
  if (status === 'Interview') return 'bg-purple-50 text-purple-800 border-purple-300'
  if (status === 'Selected') return 'bg-green-100 text-green-900 border-green-400'
  if (status === 'Rejected') return 'bg-rose-50 text-rose-800 border-rose-300'
  return 'bg-slate-50 text-slate-800'
}

onMounted(() => {
  fetchApplicants()
})
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}
</style>
