import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Public Views
import LandingView from '@/views/public/LandingView.vue'
import AboutView from '@/views/public/AboutView.vue'
import HowItWorksView from '@/views/public/HowItWorksView.vue'
import PublicJobsView from '@/views/public/PublicJobsView.vue'
import LoginView from '@/views/public/LoginView.vue'
import RegisterView from '@/views/public/RegisterView.vue'

// Student Views
import StudentDashboardView from '@/views/student/StudentDashboardView.vue'
import ResumeUploadView from '@/views/student/ResumeUploadView.vue'
import SkillsView from '@/views/student/SkillsView.vue'
import JobDetailView from '@/views/student/JobDetailView.vue'
import SavedJobsView from '@/views/student/SavedJobsView.vue'
import ApplicationsView from '@/views/student/ApplicationsView.vue'
import AIAssistantView from '@/views/student/AIAssistantView.vue'
import StudentProfileView from '@/views/student/StudentProfileView.vue'

// Company Views
import CompanyDashboardView from '@/views/company/CompanyDashboardView.vue'
import CreateJobView from '@/views/company/CreateJobView.vue'
import ManageJobsView from '@/views/company/ManageJobsView.vue'
import ApplicantsView from '@/views/company/ApplicantsView.vue'
import CompanyProfileView from '@/views/company/CompanyProfileView.vue'

// Admin Views
import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import ManageUsersView from '@/views/admin/ManageUsersView.vue'
import ManageJobsAdminView from '@/views/admin/ManageJobsAdminView.vue'
import ManageApplicationsAdminView from '@/views/admin/ManageApplicationsAdminView.vue'

const routes = [
  // Public
  { path: '/', name: 'landing', component: LandingView },
  { path: '/about', name: 'about', component: AboutView },
  { path: '/how-it-works', name: 'how-it-works', component: HowItWorksView },
  { path: '/jobs', name: 'public-jobs', component: PublicJobsView },
  { path: '/jobs/:id', name: 'job-detail', component: JobDetailView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },

  // Student
  { path: '/student/dashboard', name: 'student-dashboard', component: StudentDashboardView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/student/resume', name: 'student-resume', component: ResumeUploadView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/student/skills', name: 'student-skills', component: SkillsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/student/saved', name: 'student-saved-jobs', component: SavedJobsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/student/applications', name: 'student-applications', component: ApplicationsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/student/assistant', name: 'student-assistant', component: AIAssistantView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/student/profile', name: 'student-profile', component: StudentProfileView, meta: { requiresAuth: true, role: 'student' } },

  // Company
  { path: '/company/dashboard', name: 'company-dashboard', component: CompanyDashboardView, meta: { requiresAuth: true, role: 'company' } },
  { path: '/company/jobs', name: 'company-jobs', component: ManageJobsView, meta: { requiresAuth: true, role: 'company' } },
  { path: '/company/jobs/create', name: 'company-job-create', component: CreateJobView, meta: { requiresAuth: true, role: 'company' } },
  { path: '/company/jobs/:id/edit', name: 'company-job-edit', component: CreateJobView, meta: { requiresAuth: true, role: 'company' } },
  { path: '/company/applicants', name: 'company-applicants', component: ApplicantsView, meta: { requiresAuth: true, role: 'company' } },
  { path: '/company/profile', name: 'company-profile', component: CompanyProfileView, meta: { requiresAuth: true, role: 'company' } },

  // Admin
  { path: '/admin/dashboard', name: 'admin-dashboard', component: AdminDashboardView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/users', name: 'admin-users', component: ManageUsersView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/jobs', name: 'admin-jobs', component: ManageJobsAdminView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/applications', name: 'admin-applications', component: ManageApplicationsAdminView, meta: { requiresAuth: true, role: 'admin' } },

  // Catch All
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// Navigation Guards for Auth and Role Protection
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      return next({ name: 'login', query: { redirect: to.fullPath } })
    }

    if (to.meta.role && authStore.role !== to.meta.role && authStore.role !== 'admin') {
      // If student trying to access company or vice versa, redirect to respective dashboard
      if (authStore.role === 'student') return next({ name: 'student-dashboard' })
      if (authStore.role === 'company') return next({ name: 'company-dashboard' })
      if (authStore.role === 'admin') return next({ name: 'admin-dashboard' })
      return next('/')
    }
  }

  // If already logged in and visiting login/register, redirect to dashboard
  if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    if (authStore.isStudent) return next({ name: 'student-dashboard' })
    if (authStore.isCompany) return next({ name: 'company-dashboard' })
    if (authStore.isAdmin) return next({ name: 'admin-dashboard' })
  }

  next()
})

export default router
