<template>
  <footer class="footer-wrapper">
    <div class="container footer-container">
      <div class="footer-grid">
        <!-- Brand Info -->
        <div class="footer-col brand-col">
          <div class="footer-brand">
            <div class="logo-icon-box-sm">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                <polyline points="14 2 14 8 20 8"/>
                <path d="M10 13l2 2 4-4"/>
              </svg>
            </div>
            <span class="footer-brand-title">ResumeMatch<span class="text-gradient">.AI</span></span>
          </div>
          <p class="footer-tagline">
            Analyze your resume, extract industry skills, and match with the highest-compatibility tech roles through explainable AI.
          </p>
          <div class="status-indicator">
            <span class="pulse-dot"></span>
            <span>MySQL (XAMPP) & Local AI Engine Online</span>
          </div>
        </div>

        <!-- Student Links -->
        <div class="footer-col">
          <h4>For Students</h4>
          <ul>
            <li><router-link to="/jobs">Search Matching Jobs</router-link></li>
            <li><router-link to="/student/resume">AI Resume Analyzer</router-link></li>
            <li><router-link to="/student/skills">Extracted Skills Matrix</router-link></li>
            <li><router-link to="/student/assistant">AI Career Coach</router-link></li>
          </ul>
        </div>

        <!-- Company Links -->
        <div class="footer-col">
          <h4>For Employers</h4>
          <ul>
            <li><router-link to="/company/jobs/create">Post a Job Opening</router-link></li>
            <li><router-link to="/company/applicants">AI Candidate Ranking</router-link></li>
            <li><router-link to="/company/dashboard">Recruitment Dashboard</router-link></li>
            <li><router-link to="/register">Create Company Account</router-link></li>
          </ul>
        </div>

        <!-- Platform & Tech -->
        <div class="footer-col">
          <h4>Architecture</h4>
          <div class="tech-stack-tags">
            <span class="tech-tag">Vue 3</span>
            <span class="tech-tag">Vite</span>
            <span class="tech-tag">Flask</span>
            <span class="tech-tag">MySQL (XAMPP)</span>
            <span class="tech-tag">TF-IDF & Cosine NLP</span>
            <span class="tech-tag">JWT Auth</span>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 AI Resume Analyzer & Job Matcher. Full-Stack Production Architecture.</p>
        <div class="footer-links">
          <router-link to="/how-it-works">How It Works</router-link>
          <router-link to="/about">About System</router-link>
          <router-link to="/login">Sign In</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer-wrapper {
  background: #0f172a;
  color: #94a3b8;
  padding: 60px 0 30px;
  border-top: 1px solid #1e293b;
  margin-top: auto;
}

.footer-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 40px;
}

.brand-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon-box-sm {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.logo-icon-box-sm svg {
  width: 18px;
  height: 18px;
}

.footer-brand-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: white;
}

.footer-tagline {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #94a3b8;
  max-width: 360px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  padding: 6px 12px;
  border-radius: 9999px;
  width: fit-content;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
  animation: pulseGlow 2s infinite;
}

.footer-col h4 {
  color: white;
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.footer-col ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-col a {
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.15s ease;
}

.footer-col a:hover {
  color: #818cf8;
}

.tech-stack-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-tag {
  background: #1e293b;
  color: #cbd5e1;
  font-size: 0.775rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid #334155;
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 24px;
  border-top: 1px solid #1e293b;
  font-size: 0.85rem;
  color: #64748b;
  flex-wrap: wrap;
  gap: 16px;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-links a {
  color: #64748b;
  text-decoration: none;
}
.footer-links a:hover {
  color: #94a3b8;
}

@media (max-width: 960px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 600px) {
  .footer-grid {
    grid-template-columns: 1fr;
  }
  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
}
</style>
