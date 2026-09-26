<template>
  <div class="saved-jobs-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <div class="header-card card p-6 mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Saved Jobs</h1>
          <p class="text-slate-600 text-sm mt-1">Review and apply to bookmarked positions.</p>
        </div>
        <router-link to="/jobs" class="btn btn-secondary btn-sm">Browse More Jobs</router-link>
      </div>

      <Loader v-if="loading" text="Loading your saved positions..." />

      <EmptyState
        v-else-if="savedJobs.length === 0"
        title="No Saved Jobs"
        message="You haven't bookmarked any jobs yet. Browse available listings to save roles you are interested in."
        icon="★"
      >
        <template #action>
          <router-link to="/jobs" class="btn btn-primary btn-sm">Explore Jobs</router-link>
        </template>
      </EmptyState>

      <div v-else class="grid grid-cols-2 gap-6">
        <div v-for="job in savedJobs" :key="job.id" class="card p-6 flex flex-col justify-between">
          <div>
            <div class="flex items-start justify-between mb-2">
              <h3 class="font-bold text-slate-900 text-lg">{{ job.title }}</h3>
              <button class="text-amber-500 hover:text-slate-400 text-lg" @click="removeSaved(job.id)" title="Remove Bookmark">
                ★
              </button>
            </div>
            <div class="text-sm font-semibold text-slate-700 mb-2">{{ job.company_name }} • {{ job.location }}</div>
            <p class="text-xs text-slate-500 line-clamp-2 mb-4">{{ job.description }}</p>
          </div>

          <div class="flex items-center justify-between pt-4 border-t border-slate-100">
            <span class="badge badge-primary text-xs">{{ job.job_type }}</span>
            <router-link :to="`/jobs/${job.id}`" class="btn btn-primary btn-sm">
              View & Apply
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { studentApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import Loader from '@/components/common/Loader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const toastStore = useToastStore()
const savedJobs = ref([])
const loading = ref(true)

const fetchSavedJobs = async () => {
  loading.value = true
  try {
    const res = await studentApi.getSavedJobs()
    if (res.success) {
      savedJobs.value = res.data || []
    }
  } catch (err) {
    toastStore.error(err.message)
  } finally {
    loading.value = false
  }
}

const removeSaved = async (jobId) => {
  try {
    const res = await studentApi.toggleSaveJob(jobId)
    if (res.success) {
      savedJobs.value = savedJobs.value.filter((j) => j.id !== jobId)
      toastStore.success('Removed from saved jobs.')
    }
  } catch (err) {
    toastStore.error(err.message)
  }
}

onMounted(() => {
  fetchSavedJobs()
})
</script>

<style scoped>
@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>
