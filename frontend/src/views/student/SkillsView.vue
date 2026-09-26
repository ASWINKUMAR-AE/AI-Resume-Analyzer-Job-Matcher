<template>
  <div class="skills-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <div class="header-card card p-6 mb-8 flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Detected Technical Skills Matrix</h1>
          <p class="text-slate-600 text-sm mt-1">
            Categorized skills extracted from your resume by our NLP taxonomy engine with confidence metrics.
          </p>
        </div>
        <router-link to="/student/resume" class="btn btn-secondary btn-sm">
          Update Resume Skills
        </router-link>
      </div>

      <Loader v-if="loading" text="Loading categorized skills..." />

      <EmptyState
        v-else-if="skillsData.skills.length === 0"
        title="No Extracted Skills"
        message="Upload your resume in PDF, DOCX, or TXT format to automatically extract your skills."
        icon="⚡"
      >
        <template #action>
          <router-link to="/student/resume" class="btn btn-primary btn-sm">Upload Resume</router-link>
        </template>
      </EmptyState>

      <div v-else>
        <!-- Category Summary Bar -->
        <div class="card p-6 mb-8">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-bold text-slate-900">Total Skills Detected: {{ skillsData.total_count }}</h3>
            <span class="text-xs text-slate-500">Spanning {{ Object.keys(skillsData.categories).length }} Technology Domains</span>
          </div>

          <div class="category-pills-row flex flex-wrap gap-2">
            <span
              v-for="(skillsList, catName) in skillsData.categories"
              :key="catName"
              class="badge badge-primary py-1.5 px-3 text-xs"
            >
              {{ catName }}: <strong>{{ skillsList.length }}</strong>
            </span>
          </div>
        </div>

        <!-- Categorized Grid -->
        <div class="grid grid-cols-2 gap-6">
          <div
            v-for="(skillsList, catName) in skillsData.categories"
            :key="catName"
            class="card p-6"
          >
            <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
              <h3 class="text-base font-bold text-slate-900">{{ catName }}</h3>
              <span class="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full">
                {{ skillsList.length }} skills
              </span>
            </div>

            <div class="skill-tags-group flex flex-wrap gap-2">
              <div
                v-for="s in skillsList"
                :key="s.skill_name"
                class="skill-tag-pill"
              >
                <span class="skill-name">{{ s.skill_name }}</span>
                <span class="confidence-indicator" :title="`Confidence: ${Math.round(s.confidence * 100)}%`">
                  {{ Math.round(s.confidence * 100) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { studentApi } from '@/api'
import Loader from '@/components/common/Loader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const skillsData = ref({ skills: [], categories: {}, total_count: 0 })
const loading = ref(true)

const fetchSkills = async () => {
  loading.value = true
  try {
    const res = await studentApi.getSkills()
    if (res.success && res.data) {
      skillsData.value = res.data
    }
  } catch (err) {
    console.error('Failed to load skills:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSkills()
})
</script>

<style scoped>
.skill-tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e293b;
}

.confidence-indicator {
  font-size: 0.7rem;
  color: #6366f1;
  background: #eef2ff;
  padding: 1px 6px;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>
