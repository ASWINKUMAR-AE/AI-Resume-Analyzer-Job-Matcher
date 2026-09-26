<template>
  <div class="how-it-works-page">
    <section class="page-header gradient-mesh">
      <div class="container text-center">
        <h1 class="page-title">How <span class="text-gradient">It Works</span></h1>
        <p class="page-subtitle">A transparent overview of how our platform assists candidates and employers from start to hire.</p>
      </div>
    </section>

    <section class="section-padding bg-white">
      <div class="container">
        <!-- Student Workflow -->
        <div class="role-journey">
          <div class="journey-badge badge-primary">Student Journey</div>
          <h2 class="journey-title">4 Steps to Your Ideal Tech Role</h2>
          
          <div class="journey-steps">
            <div class="journey-step card">
              <div class="step-badge">1</div>
              <h4>Upload Your Resume</h4>
              <p>Upload your PDF or DOCX file. Our engine extracts text, contact info, and structural sections automatically.</p>
            </div>
            <div class="journey-step card">
              <div class="step-badge">2</div>
              <h4>Receive Health Score & Skills</h4>
              <p>Get a comprehensive ATS compatibility score with highlighted strengths, missing sections, and suggestions.</p>
            </div>
            <div class="journey-step card">
              <div class="step-badge">3</div>
              <h4>Explore AI Ranked Jobs</h4>
              <p>View active job listings sorted by your personalized AI compatibility score, with transparent breakdowns.</p>
            </div>
            <div class="journey-step card">
              <div class="step-badge">4</div>
              <h4>Apply & Track Progress</h4>
              <p>Submit applications in 1-click and track live status updates (Under Review, Shortlisted, Interview).</p>
            </div>
          </div>
        </div>

        <!-- Company Workflow -->
        <div class="role-journey mt-16">
          <div class="journey-badge badge-success">Company Journey</div>
          <h2 class="journey-title">Streamlined AI-Assisted Candidate Screening</h2>
          
          <div class="journey-steps">
            <div class="journey-step card">
              <div class="step-badge step-success">1</div>
              <h4>Post Job Listings</h4>
              <p>Define requirements, required tech stack, experience levels, and salary ranges in seconds.</p>
            </div>
            <div class="journey-step card">
              <div class="step-badge step-success">2</div>
              <h4>AI Candidate Ranking</h4>
              <p>Applicants are automatically ranked by compatibility score, showing matched and missing skills instantly.</p>
            </div>
            <div class="journey-step card">
              <div class="step-badge step-success">3</div>
              <h4>Review & Shortlist</h4>
              <p>Inspect parsed resumes, view cover notes, and update applicant hiring status with automated candidate feedback.</p>
            </div>
            <div class="journey-step card">
              <div class="step-badge step-success">4</div>
              <h4>Recruitment Analytics</h4>
              <p>Track applicant pipelines, average candidate match scores, and interview conversion ratios on your dashboard.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-header {
  padding: 60px 0;
  border-bottom: 1px solid #e2e8f0;
}
.page-title {
  font-size: 2.5rem;
  margin-bottom: 12px;
}
.page-subtitle {
  font-size: 1.15rem;
  color: #64748b;
  max-width: 680px;
  margin: 0 auto;
}
.role-journey {
  margin-bottom: 60px;
}
.journey-badge {
  font-size: 0.85rem;
  margin-bottom: 12px;
}
.journey-title {
  font-size: 1.8rem;
  color: #0f172a;
  margin-bottom: 30px;
}
.journey-steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.journey-step {
  padding: 24px;
}
.step-badge {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #6366f1;
  color: white;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}
.step-badge.step-success {
  background: #10b981;
}
.journey-step h4 {
  font-size: 1.05rem;
  color: #1e293b;
  margin-bottom: 8px;
}
.journey-step p {
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.5;
}
@media (max-width: 1024px) {
  .journey-steps {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 640px) {
  .journey-steps {
    grid-template-columns: 1fr;
  }
}
</style>
