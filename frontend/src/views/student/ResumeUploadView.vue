<template>
  <div class="resume-view py-8 bg-slate-50 min-h-screen">
    <div class="container max-w-5xl">
      <!-- Header -->
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">AI Resume Analyzer & ATS Audit</h1>
          <p class="text-slate-600 text-sm mt-1">
            Upload your resume (PDF, DOCX, TXT) to evaluate section completeness, extract skills, and calculate ATS health score.
          </p>
        </div>
        <button
          v-if="resumeData"
          class="btn btn-secondary btn-sm"
          @click="showUploadModal = true"
        >
          📤 Upload New Resume
        </button>
      </div>

      <!-- Upload Dropzone (shown if no resume yet or when re-uploading) -->
      <div v-if="!resumeData || showUploadModal" class="upload-dropzone-card card p-8 mb-8 text-center" :class="{ 'modal-mode': showUploadModal }">
        <div
          class="dropzone-area"
          :class="{ 'dragging': isDragging }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleFileDrop"
          @click="$refs.fileInput.click()"
        >
          <input
            ref="fileInput"
            type="file"
            accept=".pdf,.docx,.txt"
            class="hidden"
            style="display: none;"
            @change="handleFileSelect"
          />
          <div class="drop-icon">📁</div>
          <h3 class="text-lg font-bold text-slate-800 mb-1">
            Drag and drop your resume file here
          </h3>
          <p class="text-sm text-slate-500 mb-4">
            Supports PDF, DOCX, or plain TXT (Max 10 MB)
          </p>
          <button type="button" class="btn btn-primary btn-sm">
            Browse File
          </button>
        </div>

        <div v-if="uploading" class="upload-progress-box mt-4">
          <Loader :text="`Analyzing resume with NLP engine... (${uploadProgress}%)`" />
          <div class="prog-bar mt-2"><div class="prog-fill" :style="{ width: uploadProgress + '%' }"></div></div>
        </div>

        <div v-if="showUploadModal" class="mt-4 flex justify-end">
          <button class="btn btn-secondary btn-sm" @click="showUploadModal = false">Cancel</button>
        </div>
      </div>

      <!-- Loading State for Initial Fetch -->
      <Loader v-if="loading && !uploading" text="Loading resume analysis..." />

      <!-- Full Audit Dashboard (if resume exists) -->
      <template v-else-if="resumeData">
        <!-- 1. Top Score & Overview Banner -->
        <div class="score-banner card p-6 mb-8 gradient-primary text-white">
          <div class="flex items-center justify-between flex-wrap gap-4">
            <div class="flex items-center gap-6">
              <div class="score-dial">
                <span class="score-big">{{ resumeData.resume_score }}</span>
                <span class="score-sub">/ 100</span>
              </div>
              <div>
                <div class="score-badge-pill">ATS Health Score</div>
                <h2 class="text-xl font-bold text-white mt-1">{{ getScoreVerdict(resumeData.resume_score) }}</h2>
                <p class="text-sm text-indigo-100 mt-1">
                  File: <strong>{{ resumeData.file_name }}</strong> • Uploaded {{ formatDate(resumeData.created_at) }}
                </p>
              </div>
            </div>

            <div class="flex gap-3">
              <a :href="`/api/resume/download/${resumeData.id}`" class="btn btn-secondary btn-sm" target="_blank" download>
                📥 Download
              </a>
              <button class="btn btn-danger btn-sm" @click="deleteResume">
                🗑 Delete
              </button>
            </div>
          </div>
        </div>

        <!-- 2. Detected Skills Matrix -->
        <div class="card p-6 mb-8">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-slate-900">
              Extracted Technical Skills ({{ resumeData.skills?.length || 0 }})
            </h3>
            <router-link to="/student/skills" class="text-sm text-indigo-600 font-semibold hover:underline">
              View Categorized Matrix →
            </router-link>
          </div>

          <div class="skills-chips-row flex flex-wrap gap-2">
            <span
              v-for="s in resumeData.skills"
              :key="s.skill_name"
              class="badge badge-primary text-sm py-1 px-3"
            >
              {{ s.skill_name }}
              <span class="text-xs text-indigo-400 font-normal ml-1">({{ Math.round(s.confidence * 100) }}%)</span>
            </span>
          </div>
        </div>

        <!-- 3. Strengths & Weaknesses 2-Column Audit -->
        <div class="grid grid-cols-2 gap-6 mb-8">
          <!-- Strengths -->
          <div class="card p-6 border-l-4 border-l-emerald-500">
            <h3 class="text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
              <span class="text-emerald-600">✓</span> Profile Strengths
            </h3>
            <ul class="audit-list">
              <li v-for="(item, idx) in resumeData.strengths" :key="idx" class="audit-item text-slate-700">
                {{ item }}
              </li>
              <li v-if="!resumeData.strengths || resumeData.strengths.length === 0" class="text-sm text-slate-500">
                Add more detailed experience and skill categories to build strengths.
              </li>
            </ul>
          </div>

          <!-- Areas for Improvement -->
          <div class="card p-6 border-l-4 border-l-amber-500">
            <h3 class="text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
              <span class="text-amber-600">⚠</span> Recommendations & Gaps
            </h3>
            <ul class="audit-list">
              <li v-for="(item, idx) in resumeData.recommendations || resumeData.weaknesses" :key="idx" class="audit-item text-slate-700">
                {{ item }}
              </li>
              <li v-if="!resumeData.weaknesses || resumeData.weaknesses.length === 0" class="text-sm text-slate-500">
                No major structural weaknesses identified!
              </li>
            </ul>
          </div>
        </div>

        <!-- 4. Detected Sections Breakdown -->
        <div class="card p-6 mb-8">
          <h3 class="text-lg font-bold text-slate-900 mb-4">Detected Resume Sections</h3>
          <div class="grid grid-cols-3 gap-4">
            <div
              v-for="(content, sectionName) in filteredSections"
              :key="sectionName"
              class="p-4 rounded-xl border"
              :class="content ? 'bg-indigo-50/50 border-indigo-200' : 'bg-slate-50 border-slate-200 opacity-60'"
            >
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-slate-800 text-sm capitalize">{{ sectionName }}</span>
                <span :class="content ? 'text-emerald-600' : 'text-slate-400'" class="text-xs font-bold">
                  {{ content ? '✓ Detected' : '✕ Missing' }}
                </span>
              </div>
              <p class="text-xs text-slate-500 line-clamp-2">
                {{ content ? truncate(content, 90) : 'Not found in document' }}
              </p>
            </div>
          </div>
        </div>

        <!-- 5. Actionable Next Steps -->
        <div class="card p-6 bg-slate-900 text-white flex items-center justify-between flex-wrap gap-4">
          <div>
            <h3 class="text-lg font-bold text-white">Find Roles Matching Your {{ resumeData.skills?.length || 0 }} Skills</h3>
            <p class="text-sm text-slate-300 mt-1">Our AI recommendation engine matches your extracted profile with active jobs.</p>
          </div>
          <router-link to="/jobs" class="btn btn-primary">
            Explore Matching Jobs →
          </router-link>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { resumeApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import Loader from '@/components/common/Loader.vue'

const toastStore = useToastStore()

const resumeData = ref(null)
const loading = ref(true)
const uploading = ref(false)
const uploadProgress = ref(0)
const isDragging = ref(false)
const showUploadModal = ref(false)

const filteredSections = computed(() => {
  if (!resumeData.value?.parsed_sections) return {}
  const secs = resumeData.value.parsed_sections
  return {
    Summary: secs.summary,
    Skills: secs.skills,
    Experience: secs.experience,
    Education: secs.education,
    Projects: secs.projects,
    Certifications: secs.certifications
  }
})

const fetchResume = async () => {
  loading.value = true
  try {
    const res = await resumeApi.getLatestResume()
    if (res.success && res.data) {
      resumeData.value = res.data
    } else {
      resumeData.value = null
    }
  } catch (err) {
    console.error('Failed to load resume:', err)
  } finally {
    loading.value = false
  }
}

const handleFileSelect = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    uploadFile(files[0])
  }
}

const handleFileDrop = (e) => {
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) {
    uploadFile(files[0])
  }
}

const uploadFile = async (file) => {
  uploading.value = true
  uploadProgress.value = 10

  const formData = new FormData()
  formData.append('resume', file)

  try {
    const res = await resumeApi.uploadResume(formData, (progressEvent) => {
      if (progressEvent.total) {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
      }
    })

    if (res.success) {
      toastStore.success('Resume analyzed successfully!')
      resumeData.value = res.data
      showUploadModal.value = false
      await fetchResume()
    }
  } catch (err) {
    toastStore.error(err.message || 'Upload failed')
  } finally {
    uploading.value = false
    uploadProgress.value = 0
  }
}

const deleteResume = async () => {
  if (!resumeData.value || !confirm('Are you sure you want to delete this resume?')) return
  try {
    const res = await resumeApi.deleteResume(resumeData.value.id)
    if (res.success) {
      toastStore.success('Resume deleted.')
      resumeData.value = null
    }
  } catch (err) {
    toastStore.error(err.message)
  }
}

const getScoreVerdict = (score) => {
  if (score >= 85) return 'Exceptional - Ready for High-Volume ATS Applications'
  if (score >= 70) return 'Strong Profile - Minor Enhancements Recommended'
  if (score >= 50) return 'Average - Action Items Highlighted Below'
  return 'Incomplete - Requires Critical Sections & Quantifiable Results'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const truncate = (str, max) => {
  if (!str) return ''
  return str.length > max ? str.substring(0, max) + '...' : str
}

onMounted(() => {
  fetchResume()
})
</script>

<style scoped>
.dropzone-area {
  border: 2px dashed #6366f1;
  background: #f8fafc;
  border-radius: 16px;
  padding: 48px 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.dropzone-area:hover, .dropzone-area.dragging {
  background: #eef2ff;
  border-color: #4f46e5;
}
.drop-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.score-dial {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}
.score-big {
  font-size: 1.8rem;
  line-height: 1;
}
.score-sub {
  font-size: 0.7rem;
  opacity: 0.85;
}

.score-badge-pill {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.audit-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.audit-item {
  font-size: 0.875rem;
  line-height: 1.5;
  position: relative;
  padding-left: 18px;
}
.audit-item::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #6366f1;
}
@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>
