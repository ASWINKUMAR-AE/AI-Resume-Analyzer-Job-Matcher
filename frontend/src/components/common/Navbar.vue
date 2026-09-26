<template>
  <header class="navbar-wrapper">
    <div class="container navbar-container">
      <!-- Brand Logo -->
      <router-link to="/" class="brand-logo">
        <div class="logo-text-group">
          <span class="logo-title">Resume<span class="text-gradient">Match.AI</span></span>
          <span class="logo-sub">Intelligent Career Engine</span>
        </div>
      </router-link>

      <!-- Desktop Navigation Links -->
      <nav class="nav-links">
        <!-- Public Links -->
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/" class="nav-link" active-class="active">Home</router-link>
          <router-link to="/jobs" class="nav-link" active-class="active">Find Jobs</router-link>
          <router-link to="/how-it-works" class="nav-link" active-class="active">How It Works</router-link>
          <router-link to="/about" class="nav-link" active-class="active">About</router-link>
        </template>

        <!-- Student Links -->
        <template v-else-if="authStore.isStudent">
          <router-link to="/student/dashboard" class="nav-link" active-class="active">Dashboard</router-link>
          <router-link to="/student/resume" class="nav-link" active-class="active">Resume AI</router-link>
          <router-link to="/student/skills" class="nav-link" active-class="active">Skills</router-link>
          <router-link to="/jobs" class="nav-link" active-class="active">Jobs & Matches</router-link>
          <router-link to="/student/applications" class="nav-link" active-class="active">Applications</router-link>
          <router-link to="/student/assistant" class="nav-link ai-nav-link" active-class="active">
            <span class="ai-sparkle">✨</span> AI Coach
          </router-link>
        </template>

        <!-- Company Links -->
        <template v-else-if="authStore.isCompany">
          <router-link to="/company/dashboard" class="nav-link" active-class="active">Dashboard</router-link>
          <router-link to="/company/jobs" class="nav-link" active-class="active">Manage Jobs</router-link>
          <router-link to="/company/jobs/create" class="nav-link" active-class="active">+ Post Job</router-link>
          <router-link to="/company/applicants" class="nav-link" active-class="active">Applicants</router-link>
          <router-link to="/company/profile" class="nav-link" active-class="active">Profile</router-link>
        </template>

        <!-- Admin Links -->
        <template v-else-if="authStore.isAdmin">
          <router-link to="/admin/dashboard" class="nav-link" active-class="active">Dashboard</router-link>
          <router-link to="/admin/users" class="nav-link" active-class="active">Users</router-link>
          <router-link to="/admin/jobs" class="nav-link" active-class="active">Job Oversight</router-link>
          <router-link to="/admin/applications" class="nav-link" active-class="active">Applications</router-link>
        </template>
      </nav>

      <!-- User Actions & Auth Buttons -->
      <div class="nav-actions">
        <!-- Unauthenticated -->
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="btn btn-secondary btn-sm">Sign In</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Get Started Free</router-link>
        </template>

        <!-- Authenticated User Menu -->
        <template v-else>
          <div class="user-chip">
            <div class="user-avatar">
              {{ (authStore.userName || 'U').charAt(0).toUpperCase() }}
            </div>
            <div class="user-info-text">
              <span class="user-name">{{ authStore.userName }}</span>
              <span class="role-badge" :class="'role-' + authStore.role">{{ authStore.role }}</span>
            </div>
          </div>
          <button class="btn btn-secondary btn-sm" @click="handleLogout" title="Sign Out">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            <span class="hidden-mobile">Logout</span>
          </button>
        </template>

        <!-- Mobile Menu Button -->
        <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>

    <!-- Mobile Navigation Drawer -->
    <div v-if="mobileMenuOpen" class="mobile-menu">
      <div class="mobile-links" @click="mobileMenuOpen = false">
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/" class="mobile-nav-link">Home</router-link>
          <router-link to="/jobs" class="mobile-nav-link">Find Jobs</router-link>
          <router-link to="/how-it-works" class="mobile-nav-link">How It Works</router-link>
          <router-link to="/about" class="mobile-nav-link">About</router-link>
          <router-link to="/login" class="mobile-nav-link">Sign In</router-link>
          <router-link to="/register" class="mobile-nav-link text-indigo-600 font-bold">Register</router-link>
        </template>
        <template v-else-if="authStore.isStudent">
          <router-link to="/student/dashboard" class="mobile-nav-link">Dashboard</router-link>
          <router-link to="/student/resume" class="mobile-nav-link">Resume AI</router-link>
          <router-link to="/student/skills" class="mobile-nav-link">Skills</router-link>
          <router-link to="/jobs" class="mobile-nav-link">Jobs & Matches</router-link>
          <router-link to="/student/applications" class="mobile-nav-link">Applications</router-link>
          <router-link to="/student/saved" class="mobile-nav-link">Saved Jobs</router-link>
          <router-link to="/student/assistant" class="mobile-nav-link">AI Assistant</router-link>
          <router-link to="/student/profile" class="mobile-nav-link">My Profile</router-link>
        </template>
        <template v-else-if="authStore.isCompany">
          <router-link to="/company/dashboard" class="mobile-nav-link">Dashboard</router-link>
          <router-link to="/company/jobs" class="mobile-nav-link">Manage Jobs</router-link>
          <router-link to="/company/jobs/create" class="mobile-nav-link">+ Post Job</router-link>
          <router-link to="/company/applicants" class="mobile-nav-link">Applicants</router-link>
          <router-link to="/company/profile" class="mobile-nav-link">Company Profile</router-link>
        </template>
        <template v-else-if="authStore.isAdmin">
          <router-link to="/admin/dashboard" class="mobile-nav-link">Dashboard</router-link>
          <router-link to="/admin/users" class="mobile-nav-link">Manage Users</router-link>
          <router-link to="/admin/jobs" class="mobile-nav-link">Job Oversight</router-link>
          <router-link to="/admin/applications" class="mobile-nav-link">Applications</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const authStore = useAuthStore()
const toastStore = useToastStore()
const router = useRouter()
const mobileMenuOpen = ref(false)

const handleLogout = () => {
  authStore.logout()
  toastStore.info('You have been signed out.')
  router.push('/login')
}
</script>

<style scoped>
.navbar-wrapper {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid #e2e8f0;
  height: 72px;
  display: flex;
  align-items: center;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}

.logo-icon-box svg {
  width: 22px;
  height: 22px;
}

.logo-text-group {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.15;
}

.logo-sub {
  font-size: 0.675rem;
  font-weight: 600;
  color: #64748b;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: #475569;
  padding: 8px 14px;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.15s ease;
}

.nav-link:hover {
  color: #4f46e5;
  background: #f1f5f9;
}

.nav-link.active {
  color: #4f46e5;
  background: #eef2ff;
}

.ai-nav-link {
  color: #7c3aed;
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
}
.ai-nav-link:hover, .ai-nav-link.active {
  background: #ede9fe;
  color: #6d28d9;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 12px 4px 4px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  font-weight: 700;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.user-name {
  font-size: 0.825rem;
  font-weight: 700;
  color: #1e293b;
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.role-badge {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 1px 6px;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.role-student {
  background: #e0e7ff;
  color: #3730a3;
}
.role-company {
  background: #dcfce7;
  color: #166534;
}
.role-admin {
  background: #fef3c7;
  color: #92400e;
}

.mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 6px;
}
.mobile-toggle span {
  width: 22px;
  height: 2px;
  background: #334155;
  border-radius: 2px;
}

.mobile-menu {
  display: none;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 16px;
}
.mobile-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.mobile-nav-link {
  font-weight: 600;
  color: #334155;
  text-decoration: none;
  padding: 10px 14px;
  border-radius: 8px;
}
.mobile-nav-link:hover {
  background: #f1f5f9;
}

@media (max-width: 960px) {
  .nav-links {
    display: none;
  }
  .mobile-toggle {
    display: flex;
  }
  .mobile-menu {
    display: block;
  }
  .hidden-mobile {
    display: none;
  }
}
</style>
