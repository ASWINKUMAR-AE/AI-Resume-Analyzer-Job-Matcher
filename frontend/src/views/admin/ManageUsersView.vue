<template>
  <div class="admin-users-page py-8 bg-slate-50 min-h-screen">
    <div class="container">
      <div class="header-card card p-6 mb-8 flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">User Account Management</h1>
          <p class="text-slate-600 text-sm mt-1">Audit platform accounts and update user active/inactive statuses.</p>
        </div>

        <div class="flex gap-2">
          <input
            v-model="searchQuery"
            type="text"
            class="form-input text-xs w-60"
            placeholder="Search name or email..."
            @input="fetchUsers"
          />
          <select v-model="selectedRole" class="form-select text-xs w-36" @change="fetchUsers">
            <option value="all">All Roles</option>
            <option value="student">Students</option>
            <option value="company">Companies</option>
            <option value="admin">Admins</option>
          </select>
        </div>
      </div>

      <Loader v-if="loading" text="Loading platform users..." />

      <div v-else class="card overflow-hidden">
        <div class="table-responsive">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
                <th class="p-4">Name & Email</th>
                <th class="p-4">Role</th>
                <th class="p-4">Account Status</th>
                <th class="p-4">Created Date</th>
                <th class="p-4 text-right">Moderation Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-sm">
              <tr v-for="u in users" :key="u.id" class="hover:bg-slate-50/80 transition">
                <td class="p-4">
                  <strong class="text-slate-900 block">{{ u.name }}</strong>
                  <span class="text-xs text-slate-500">{{ u.email }}</span>
                </td>
                <td class="p-4">
                  <span class="badge" :class="'badge-' + (u.role === 'company' ? 'success' : (u.role === 'admin' ? 'warning' : 'primary'))">
                    {{ u.role }}
                  </span>
                </td>
                <td class="p-4">
                  <span class="badge" :class="u.status === 'active' ? 'badge-success' : 'badge-danger'">
                    {{ u.status }}
                  </span>
                </td>
                <td class="p-4 text-xs text-slate-500">
                  {{ formatDate(u.created_at) }}
                </td>
                <td class="p-4 text-right">
                  <button
                    v-if="u.role !== 'admin'"
                    class="btn btn-sm text-xs"
                    :class="u.status === 'active' ? 'btn-danger' : 'btn-primary'"
                    @click="toggleUserStatus(u)"
                  >
                    {{ u.status === 'active' ? 'Deactivate' : 'Activate' }}
                  </button>
                  <span v-else class="text-xs text-slate-400">System Admin</span>
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
import { adminApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import Loader from '@/components/common/Loader.vue'

const toastStore = useToastStore()
const users = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedRole = ref('all')

const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      q: searchQuery.value,
      role: selectedRole.value
    }
    const res = await adminApi.getUsers(params)
    if (res.success) {
      users.value = res.data || []
    }
  } catch (err) {
    toastStore.error(err.message)
  } finally {
    loading.value = false
  }
}

const toggleUserStatus = async (user) => {
  const newStatus = user.status === 'active' ? 'inactive' : 'active'
  try {
    const res = await adminApi.updateUserStatus(user.id, newStatus)
    if (res.success) {
      user.status = newStatus
      toastStore.success(`User status updated to ${newStatus}`)
    }
  } catch (err) {
    toastStore.error(err.message)
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
  fetchUsers()
})
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}
</style>
