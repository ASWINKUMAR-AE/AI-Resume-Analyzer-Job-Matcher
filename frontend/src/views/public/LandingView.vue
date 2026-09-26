<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section gradient-mesh">
      <div class="container hero-container">
        <div class="hero-badge">
          <span class="sparkle-icon">✨</span>
          <span>Next-Generation Career AI & ATS Matching</span>
        </div>
        
        <h1 class="hero-title">
          Analyze Your Resume. Discover Your Skills. <br />
          <span class="text-gradient">Find Your Best-Matching Jobs.</span>
        </h1>
        
        <p class="hero-description">
          Bridging candidate talent and hiring teams through explainable AI matching, 
          automated skill extraction, ATS resume health scoring, and actionable learning insights.
        </p>

        <div class="hero-actions">
          <router-link to="/student/resume" class="btn btn-primary btn-lg">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            Analyze Resume & Match Jobs
          </router-link>
          
          <router-link to="/jobs" class="btn btn-secondary btn-lg">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            Explore 6+ Active Tech Jobs
          </router-link>
        </div>

        <!-- Quick Demo Accounts Banner for Instant Evaluation -->
        <div class="demo-access-banner">
          <div class="demo-badge">🚀 Instant Demo Logins</div>
          <div class="demo-buttons-row">
            <button class="btn btn-sm demo-chip" @click="quickLogin('alex.student@example.com', 'Student@123')">
              👨‍🎓 Student: Alex Rivera
            </button>
            <button class="btn btn-sm demo-chip" @click="quickLogin('hr@technova.com', 'Company@123')">
              🏢 Company: TechNova HR
            </button>
            <button class="btn btn-sm demo-chip" @click="quickLogin('admin@airesume.com', 'Admin@123')">
              ⚡ Admin: Administrator
            </button>
          </div>
        </div>

        <!-- Interactive AI Match Visualizer Card -->
        <div class="hero-preview-card card card-glass">
          <div class="preview-header">
            <div class="preview-status">
              <span class="live-dot"></span>
              <span>Live AI Match Engine Demo</span>
            </div>
            <div class="match-pill match-high">
              ⚡ 91.5% Compatibility Match
            </div>
          </div>

          <div class="preview-grid">
            <div class="preview-col">
              <h4>Candidate Profile Extracted</h4>
              <div class="skill-chips-group">
                <span class="skill-chip matched">✓ Python</span>
                <span class="skill-chip matched">✓ Vue.js</span>
                <span class="skill-chip matched">✓ Flask</span>
                <span class="skill-chip matched">✓ MySQL</span>
                <span class="skill-chip matched">✓ REST API</span>
                <span class="skill-chip matched">✓ Git</span>
              </div>
            </div>

            <div class="preview-divider">
              <svg class="w-6 h-6 text-indigo-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </div>

            <div class="preview-col">
              <h4>Target Role: Full Stack Developer</h4>
              <div class="score-progress-list">
                <div class="prog-row">
                  <span>Skill Overlap (45% wt)</span>
                  <div class="prog-bar"><div class="prog-fill" style="width: 95%;"></div></div>
                  <span>95%</span>
                </div>
                <div class="prog-row">
                  <span>TF-IDF Semantic Text (30% wt)</span>
                  <div class="prog-bar"><div class="prog-fill" style="width: 88%;"></div></div>
                  <span>88%</span>
                </div>
                <div class="prog-row">
                  <span>Experience Alignment (15% wt)</span>
                  <div class="prog-bar"><div class="prog-fill" style="width: 85%;"></div></div>
                  <span>85%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Key Core Features Grid -->
    <section class="section-padding bg-white">
      <div class="container">
        <div class="section-header text-center">
          <h2 class="section-title">End-to-End Intelligent Recruitment Ecosystem</h2>
          <p class="section-subtitle">
            Engineered with deep NLP parsing, transparent algorithms, and multi-role dashboards for students and employers.
          </p>
        </div>

        <div class="features-grid">
          <!-- Feature 1 -->
          <div class="feature-card card card-interactive">
            <div class="feature-icon bg-indigo-50 text-indigo-600">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <h3>Deep Resume Parser</h3>
            <p>Extracts text from PDF, DOCX, and TXT files, categorizing sections: Summary, Skills, Work History, Education, and Projects.</p>
          </div>

          <!-- Feature 2 -->
          <div class="feature-card card card-interactive">
            <div class="feature-icon bg-purple-50 text-purple-600">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            </div>
            <h3>Skill Taxonomy & Aliases</h3>
            <p>Configurable dictionary mapping variations (e.g. <em>Vue, VueJS, Vue.js</em>) to canonical skills with confidence weighting.</p>
          </div>

          <!-- Feature 3 -->
          <div class="feature-card card card-interactive">
            <div class="feature-icon bg-emerald-50 text-emerald-600">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                <line x1="9" y1="9" x2="9.01" y2="9"/>
                <line x1="15" y1="9" x2="15.01" y2="9"/>
              </svg>
            </div>
            <h3>ATS Resume Health Score</h3>
            <p>Scores resumes from 0-100% on section completeness, action verbs, quantifiable metrics, profile links, and formatting clarity.</p>
          </div>

          <!-- Feature 4 -->
          <div class="feature-card card card-interactive">
            <div class="feature-icon bg-cyan-50 text-cyan-600">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                <line x1="12" y1="22.08" x2="12" y2="12"/>
              </svg>
            </div>
            <h3>TF-IDF & Cosine Matching</h3>
            <p>Calculates semantic similarity between candidate resumes and job listings without black-box hallucinations.</p>
          </div>

          <!-- Feature 5 -->
          <div class="feature-card card card-interactive">
            <div class="feature-icon bg-amber-50 text-amber-600">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <h3>Missing Skill Gap Analysis</h3>
            <p>Instantly highlights missing skills for any role with targeted learning pathways to boost hiring probability.</p>
          </div>

          <!-- Feature 6 -->
          <div class="feature-card card card-interactive">
            <div class="feature-icon bg-rose-50 text-rose-600">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
              </svg>
            </div>
            <h3>Grounded AI Career Coach</h3>
            <p>Interactive student chat assistant that references your real resume, skills, and matched jobs with 100% offline fallback.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="section-padding bg-slate-50">
      <div class="container">
        <div class="section-header text-center">
          <h2 class="section-title">How ResumeMatch.AI Works</h2>
          <p class="section-subtitle">A seamless journey from initial upload to job application and candidate shortlisting.</p>
        </div>

        <div class="workflow-steps">
          <div class="step-card">
            <div class="step-number">1</div>
            <h4>Upload Resume</h4>
            <p>Drop your PDF or DOCX file. Our engine extracts text, contact info, and structural sections.</p>
          </div>

          <div class="step-connector"></div>

          <div class="step-card">
            <div class="step-number">2</div>
            <h4>Skill Extraction & Audit</h4>
            <p>AI identifies technical competencies, evaluates ATS formatting, and gives actionable improvements.</p>
          </div>

          <div class="step-connector"></div>

          <div class="step-card">
            <div class="step-number">3</div>
            <h4>AI Job Matching</h4>
            <p>Jobs are dynamically scored based on skill overlap, semantic similarity, and experience level.</p>
          </div>

          <div class="step-connector"></div>

          <div class="step-card">
            <div class="step-number">4</div>
            <h4>Apply & Get Hired</h4>
            <p>Submit with 1-click. Employers review ranked applicant lists and update candidate hiring status.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action Banner -->
    <section class="cta-section gradient-dark text-white text-center">
      <div class="container">
        <h2 class="cta-title">Ready to Find Your Highest-Matching Job?</h2>
        <p class="cta-text">Join thousands of students and companies accelerating recruitment with explainable AI.</p>
        <div class="cta-actions">
          <router-link to="/register" class="btn btn-primary btn-lg">Create Free Account</router-link>
          <router-link to="/jobs" class="btn btn-secondary btn-lg">Browse Open Positions</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const authStore = useAuthStore()
const toastStore = useToastStore()
const router = useRouter()

const quickLogin = async (email, password) => {
  const res = await authStore.login(email, password)
  if (res.success) {
    toastStore.success(`Logged in as ${authStore.userName} (${authStore.role})!`)
    if (authStore.isStudent) router.push('/student/dashboard')
    else if (authStore.isCompany) router.push('/company/dashboard')
    else if (authStore.isAdmin) router.push('/admin/dashboard')
  } else {
    toastStore.error(res.message || 'Login failed')
  }
}
</script>

<style scoped>
.hero-section {
  padding: 80px 0 60px;
  border-bottom: 1px solid #e2e8f0;
}

.hero-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: #ffffff;
  border: 1px solid #e0e7ff;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #4f46e5;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.12);
  margin-bottom: 24px;
}

.hero-title {
  font-size: 3.2rem;
  line-height: 1.15;
  font-weight: 800;
  color: #0f172a;
  max-width: 900px;
  margin-bottom: 20px;
}

.hero-description {
  font-size: 1.15rem;
  color: #475569;
  max-width: 720px;
  line-height: 1.6;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 36px;
}

.demo-access-banner {
  background: rgba(255, 255, 255, 0.9);
  border: 1px dashed #6366f1;
  border-radius: 12px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 40px;
}

.demo-badge {
  font-size: 0.85rem;
  font-weight: 700;
  color: #4338ca;
}

.demo-buttons-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.demo-chip {
  background: #eef2ff;
  color: #3730a3;
  border: 1px solid #c7d2fe;
  font-size: 0.825rem;
  transition: all 0.15s ease;
}
.demo-chip:hover {
  background: #e0e7ff;
  transform: translateY(-1px);
}

.hero-preview-card {
  width: 100%;
  max-width: 860px;
  padding: 24px 32px;
  border-radius: 20px;
  box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 16px;
  margin-bottom: 20px;
}

.preview-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  font-weight: 700;
  color: #334155;
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.preview-grid {
  display: grid;
  grid-template-columns: 1fr auto 1.2fr;
  gap: 24px;
  align-items: center;
}

.preview-col h4 {
  font-size: 0.9rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 12px;
}

.skill-chips-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-chip {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}

.preview-divider {
  display: flex;
  align-items: center;
  justify-content: center;
}

.score-progress-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.prog-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.775rem;
  font-weight: 600;
  color: #475569;
}

.prog-bar {
  flex: 1;
  height: 6px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.prog-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1 0%, #10b981 100%);
  border-radius: 999px;
}

/* Features Grid */
.section-padding {
  padding: 80px 0;
}

.section-header {
  margin-bottom: 50px;
}

.section-title {
  font-size: 2.3rem;
  color: #0f172a;
  margin-bottom: 12px;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  max-width: 650px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.feature-card {
  padding: 30px;
  border-radius: 16px;
}

.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.feature-icon svg {
  width: 24px;
  height: 24px;
}

.feature-card h3 {
  font-size: 1.2rem;
  color: #1e293b;
  margin-bottom: 10px;
}

.feature-card p {
  font-size: 0.925rem;
  color: #64748b;
  line-height: 1.6;
}

/* Workflow Steps */
.workflow-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.step-card {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
}

.step-number {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #6366f1;
  color: white;
  font-weight: 800;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.step-card h4 {
  font-size: 1.05rem;
  color: #0f172a;
  margin-bottom: 8px;
}

.step-card p {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.5;
}

.step-connector {
  width: 30px;
  height: 2px;
  background: #cbd5e1;
}

/* CTA */
.cta-section {
  padding: 80px 0;
}

.cta-title {
  font-size: 2.4rem;
  color: white;
  margin-bottom: 14px;
}

.cta-text {
  font-size: 1.15rem;
  color: #cbd5e1;
  margin-bottom: 32px;
}

.cta-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .workflow-steps {
    flex-direction: column;
  }
  .step-connector {
    width: 2px;
    height: 24px;
  }
  .preview-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 640px) {
  .hero-title {
    font-size: 2.2rem;
  }
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
