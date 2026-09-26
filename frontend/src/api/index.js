import apiClient from './axios'

// --- Student APIs ---
export const studentApi = {
  getProfile: (userId) => apiClient.get('/student/profile', { params: { user_id: userId } }),
  updateProfile: (data) => apiClient.put('/student/profile', data),
  getDashboard: () => apiClient.get('/student/dashboard'),
  getSkills: () => apiClient.get('/student/skills'),
  getSavedJobs: () => apiClient.get('/student/saved-jobs'),
  toggleSaveJob: (jobId) => apiClient.post(`/student/saved-jobs/${jobId}`)
}

// --- Company APIs ---
export const companyApi = {
  getProfile: (companyId) => apiClient.get('/company/profile', { params: { company_id: companyId } }),
  updateProfile: (data) => apiClient.put('/company/profile', data),
  getDashboard: () => apiClient.get('/company/dashboard')
}

// --- Jobs APIs ---
export const jobsApi = {
  getJobs: (params) => apiClient.get('/jobs', { params }),
  getJobDetail: (jobId) => apiClient.get(`/jobs/${jobId}`),
  createJob: (data) => apiClient.post('/jobs', data),
  updateJob: (jobId, data) => apiClient.put(`/jobs/${jobId}`, data),
  deleteJob: (jobId) => apiClient.delete(`/jobs/${jobId}`)
}

// --- Resume APIs ---
export const resumeApi = {
  uploadResume: (formData, onUploadProgress) => {
    return apiClient.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress
    })
  },
  getLatestResume: (studentId) => apiClient.get('/resume', { params: { student_id: studentId } }),
  deleteResume: (resumeId) => apiClient.delete(`/resume/${resumeId}`),
  getDownloadUrl: (resumeId) => `/api/resume/download/${resumeId}`
}

// --- Applications APIs ---
export const applicationsApi = {
  applyForJob: (jobId, data) => apiClient.post(`/applications/jobs/${jobId}/apply`, data),
  getStudentApplications: () => apiClient.get('/applications/student'),
  getCompanyApplications: (params) => apiClient.get('/applications/company', { params }),
  getApplicationDetail: (appId) => apiClient.get(`/applications/${appId}`),
  updateStatus: (appId, status) => apiClient.put(`/applications/${appId}/status`, { status })
}

// --- AI & Assistant APIs ---
export const aiApi = {
  getRecommendations: (limit = 10) => apiClient.get('/ai/recommendations', { params: { limit } }),
  matchPreview: (jobId, studentId) => apiClient.post('/ai/match-preview', { job_id: jobId, student_id: studentId }),
  sendChatMessage: (message, jobId) => apiClient.post('/ai/chat', { message, job_id: jobId })
}

// --- Admin APIs ---
export const adminApi = {
  getDashboard: () => apiClient.get('/admin/dashboard'),
  getUsers: (params) => apiClient.get('/admin/users', { params }),
  updateUserStatus: (userId, status) => apiClient.put(`/admin/users/${userId}/status`, { status }),
  getJobs: () => apiClient.get('/admin/jobs'),
  deleteJob: (jobId) => apiClient.delete(`/admin/jobs/${jobId}`),
  getApplications: () => apiClient.get('/admin/applications')
}

// --- System Health API ---
export const healthApi = {
  check: () => apiClient.get('/health')
}
