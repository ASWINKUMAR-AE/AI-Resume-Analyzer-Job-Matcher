<template>
  <div class="about-page">
    <section class="page-header gradient-mesh">
      <div class="container text-center">
        <h1 class="page-title">About <span class="text-gradient">ResumeMatch.AI</span></h1>
        <p class="page-subtitle">
          Transparent, explainable, and privacy-conscious artificial intelligence designed to empower students and recruitment teams.
        </p>
      </div>
    </section>

    <section class="section-padding bg-white">
      <div class="container">
        <div class="content-columns">
          <div class="content-card card">
            <h3>🎯 Our Mission</h3>
            <p>
              Traditional applicant tracking systems often act as black boxes, filtering out promising talent based on rigid keyword matching. 
              <strong>ResumeMatch.AI</strong> was created to demystify recruitment technology by providing <strong>explainable AI scoring</strong>.
              Students see exactly why they matched with a job, which skills they possess, and which skills they need to learn next.
            </p>
          </div>

          <div class="content-card card">
            <h3>🔬 Explainable AI Methodology</h3>
            <p>
              Rather than relying on opaque predictions, our hybrid engine combines classical natural language processing (NLP), 
              TF-IDF vectorization, Cosine Similarity, and weighted domain heuristics:
            </p>
            <ul class="methodology-list">
              <li><strong>45% Skill Overlap:</strong> Evaluates canonical and aliased technical competencies.</li>
              <li><strong>30% Semantic Text Similarity:</strong> Measures TF-IDF contextual alignment between resume text and role responsibilities.</li>
              <li><strong>15% Experience Alignment:</strong> Validates career level and project tenure.</li>
              <li><strong>10% Education & Prerequisites:</strong> Analyzes degree level and academic background.</li>
            </ul>
          </div>
        </div>

        <div class="privacy-card card bg-slate-50 mt-8">
          <h3>🔒 Data Privacy & Offline Resilience</h3>
          <p>
            Your resume files and candidate profiles are private. We do not sell candidate data. Furthermore, our core NLP parsing, 
            skill extraction, and matching algorithms execute locally without requiring mandatory external cloud LLMs, ensuring 
            enterprise-grade speed, privacy, and 100% offline availability.
          </p>
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
.content-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}
.content-card {
  padding: 32px;
}
.content-card h3, .privacy-card h3 {
  font-size: 1.3rem;
  margin-bottom: 14px;
  color: #0f172a;
}
.content-card p, .privacy-card p {
  color: #475569;
  line-height: 1.7;
  font-size: 0.95rem;
}
.methodology-list {
  margin-top: 14px;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.methodology-list li {
  padding-left: 18px;
  position: relative;
  font-size: 0.9rem;
  color: #334155;
}
.methodology-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #6366f1;
  font-size: 1.4rem;
  line-height: 1;
}
.privacy-card {
  padding: 32px;
  margin-top: 30px;
  border-left: 4px solid #6366f1;
}
@media (max-width: 768px) {
  .content-columns {
    grid-template-columns: 1fr;
  }
}
</style>
