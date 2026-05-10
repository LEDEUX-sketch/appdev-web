<template>
  <div class="landing-page">
    <!-- Animated background -->
    <div class="bg-grid" aria-hidden="true"></div>
    <div class="bg-glow bg-glow--1" aria-hidden="true"></div>
    <div class="bg-glow bg-glow--2" aria-hidden="true"></div>

    <!-- Navigation bar -->
    <header class="landing-nav">
      <div class="nav-brand">
        <div class="brand-mark" aria-hidden="true">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect x="2" y="2" width="28" height="28" rx="8" stroke="url(#brandGrad)" stroke-width="2.5" fill="none"/>
            <path d="M10 16l4 4 8-8" stroke="url(#brandGrad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="brandGrad" x1="0" y1="0" x2="32" y2="32">
                <stop stop-color="#06d6a0"/>
                <stop offset="1" stop-color="#8338ec"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span class="brand-text">SOAVS</span>
      </div>

    </header>

    <!-- Hero Section -->
    <section class="hero" id="hero">
      <div class="hero-content">
        <div class="hero-badge anim-reveal" style="--delay: 0s">
          <span class="badge-dot" aria-hidden="true"></span>
          Student Organization Automated Voting System
        </div>
        <h1 class="hero-title anim-reveal" style="--delay: 0.15s">
          Vote <span class="text-gradient">smarter.</span><br/>
          Lead <span class="text-gradient-alt">stronger.</span>
        </h1>
        <p class="hero-subtitle anim-reveal" style="--delay: 0.3s">
          Transparent, tamper-proof elections for student organizations — right from your phone.
          Cast your ballot in seconds and track live results with confidence.
        </p>
        <div class="hero-actions anim-reveal" style="--delay: 0.45s">
          <a
            href="https://expo.dev/accounts/aoie3/projects/student-vote/builds/193e84e3-8a0d-4db5-89bb-733893c73cac"
            target="_blank"
            rel="noopener noreferrer"
            class="btn-download"
            id="download-apk-btn"
          >
            <i class="fa-brands fa-android"></i>
            Download APK
            <span class="btn-arrow" aria-hidden="true">↗</span>
          </a>

        </div>
      </div>

      <div class="hero-visual anim-reveal" style="--delay: 0.5s">
        <div class="phone-mockup">
          <div class="phone-screen">
            <div class="mock-header">
              <div class="mock-status-bar">
                <span>9:41</span>
                <div class="mock-icons"><span></span><span></span><span></span></div>
              </div>
              <div class="mock-app-bar">
                <div class="mock-avatar"></div>
                <span>Student Vote</span>
              </div>
            </div>
            <div class="mock-body">
              <div class="mock-card mock-card--active">
                <div class="mock-card-icon">🗳️</div>
                <div class="mock-card-text">
                  <strong>SSG Elections 2025</strong>
                  <span>Voting ends May 15</span>
                </div>
                <div class="mock-badge-live">LIVE</div>
              </div>
              <div class="mock-card">
                <div class="mock-card-icon">📊</div>
                <div class="mock-card-text">
                  <strong>View Results</strong>
                  <span>Real-time tallying</span>
                </div>
              </div>
              <div class="mock-card">
                <div class="mock-card-icon">👤</div>
                <div class="mock-card-text">
                  <strong>Candidates</strong>
                  <span>12 running this year</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features" id="features">
      <div class="features-grid">
        <div class="feature-card anim-reveal" style="--delay: 0s" v-for="(f, i) in features" :key="i">
          <div class="feature-icon" :style="{ background: f.gradient }">
            <i :class="f.icon"></i>
          </div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.description }}</p>
        </div>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="cta-banner anim-reveal" style="--delay: 0.1s" id="cta">
      <div class="cta-inner">
        <h2>Ready to vote?</h2>
        <p>Download the SOAVS mobile app and participate in your organization's elections today.</p>
        <a
          href="https://expo.dev/accounts/aoie3/projects/student-vote/builds/193e84e3-8a0d-4db5-89bb-733893c73cac"
          target="_blank"
          rel="noopener noreferrer"
          class="btn-download btn-download--lg"
          id="download-apk-btn-bottom"
        >
          <i class="fa-brands fa-android"></i>
          Get the App
          <span class="btn-arrow" aria-hidden="true">↗</span>
        </a>
      </div>
    </section>

    <!-- Footer -->
    <footer class="landing-footer">
      <p>&copy; {{ new Date().getFullYear() }} SOAVS &mdash; Student Organization Automated Voting System</p>
    </footer>
  </div>
</template>

<script setup>
const features = [
  {
    icon: 'fa-solid fa-shield-halved',
    title: 'Secure & Tamper-Proof',
    description: 'JWT-authenticated sessions and one-vote-per-student enforcement ensure election integrity.',
    gradient: 'linear-gradient(135deg, #06d6a0, #0b8a6f)'
  },
  {
    icon: 'fa-solid fa-bolt',
    title: 'Real-Time Results',
    description: 'Watch live tallies as votes pour in. Instant, transparent results with zero delay.',
    gradient: 'linear-gradient(135deg, #8338ec, #5a1eb8)'
  },
  {
    icon: 'fa-solid fa-mobile-screen-button',
    title: 'Vote on Mobile',
    description: 'A sleek native app lets students vote from anywhere — no laptops required.',
    gradient: 'linear-gradient(135deg, #ff6b6b, #c0392b)'
  },
  {
    icon: 'fa-solid fa-chart-pie',
    title: 'Admin Dashboard',
    description: 'Manage elections, candidates, and voter rolls from a powerful web-based control panel.',
    gradient: 'linear-gradient(135deg, #4ecdc4, #2d8f88)'
  }
]
</script>

<style scoped>
/* ─── GOOGLE FONT OVERRIDE ─── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

.landing-page {
  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'Outfit', sans-serif;
  --accent-1: #06d6a0;
  --accent-2: #8338ec;
  --surface: rgba(15, 23, 42, 0.65);
  --surface-border: rgba(255, 255, 255, 0.06);
  font-family: var(--font-body);
  position: relative;
  overflow-x: hidden;
  min-height: 100vh;
}

/* ─── BACKGROUND ─── */
.bg-grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 64px 64px;
  pointer-events: none;
  z-index: 0;
}
.bg-glow {
  position: fixed;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(140px);
  opacity: 0.18;
  pointer-events: none;
  z-index: 0;
}
.bg-glow--1 {
  top: -120px;
  right: -80px;
  background: var(--accent-2);
  animation: floatGlow 12s ease-in-out infinite alternate;
}
.bg-glow--2 {
  bottom: -200px;
  left: -120px;
  background: var(--accent-1);
  animation: floatGlow 14s ease-in-out infinite alternate-reverse;
}

/* ─── ANIMATION FOUNDATIONS ─── */
.anim-reveal {
  opacity: 0;
  transform: translateY(32px);
  animation: revealUp 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  animation-delay: var(--delay, 0s);
}

@keyframes revealUp {
  to { opacity: 1; transform: translateY(0); }
}
@keyframes floatGlow {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(40px, 30px) scale(1.15); }
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ─── NAV BAR ─── */
.landing-nav {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 48px;
  max-width: 1280px;
  margin: 0 auto;
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.brand-text {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 22px;
  letter-spacing: 2px;
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.nav-link {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: 14px;
  color: #94a3b8;
  text-decoration: none;
  padding: 10px 24px;
  border: 1px solid var(--surface-border);
  border-radius: 999px;
  transition: all 0.3s;
}
.nav-link:hover {
  color: #f8fafc;
  border-color: var(--accent-1);
  background: rgba(6, 214, 160, 0.08);
}

/* ─── HERO ─── */
.hero {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 64px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 48px 100px;
}
.hero-content {
  flex: 1;
  max-width: 600px;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  font-weight: 500;
  color: var(--accent-1);
  background: rgba(6, 214, 160, 0.08);
  border: 1px solid rgba(6, 214, 160, 0.2);
  padding: 8px 18px;
  border-radius: 999px;
  margin-bottom: 28px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-1);
  animation: pulse 2s ease-in-out infinite;
}
.hero-title {
  font-family: var(--font-display);
  font-size: clamp(40px, 5.5vw, 72px);
  font-weight: 700;
  line-height: 1.08;
  letter-spacing: -1.5px;
  margin-bottom: 24px;
}
.text-gradient {
  background: linear-gradient(135deg, var(--accent-1), #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-gradient-alt {
  background: linear-gradient(135deg, var(--accent-2), #ff6b6b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-subtitle {
  font-size: 18px;
  line-height: 1.7;
  color: #94a3b8;
  margin-bottom: 40px;
  max-width: 480px;
}

/* ─── BUTTONS ─── */
.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.btn-download {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 15px;
  padding: 14px 32px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--accent-1), #0b8a6f);
  color: #0f172a;
  text-decoration: none;
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow:
    0 0 0 0 rgba(6, 214, 160, 0),
    0 4px 16px rgba(6, 214, 160, 0.2);
}
.btn-download:hover {
  transform: translateY(-2px);
  box-shadow:
    0 0 24px rgba(6, 214, 160, 0.25),
    0 8px 24px rgba(6, 214, 160, 0.3);
}
.btn-download--lg {
  padding: 18px 40px;
  font-size: 17px;
  border-radius: 14px;
}
.btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-body);
  font-weight: 500;
  font-size: 15px;
  padding: 14px 28px;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid var(--surface-border);
  color: #e2e8f0;
  text-decoration: none;
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.btn-ghost:hover {
  border-color: rgba(255, 255, 255, 0.15);
  background: rgba(30, 41, 59, 0.9);
  transform: translateY(-2px);
}
.btn-arrow {
  font-size: 18px;
  transition: transform 0.25s;
}
.btn-download:hover .btn-arrow,
.btn-ghost:hover .btn-arrow {
  transform: translate(3px, -2px);
}

/* ─── PHONE MOCKUP ─── */
.hero-visual {
  flex: 0 0 auto;
}
.phone-mockup {
  width: 280px;
  height: 560px;
  background: #0c1222;
  border-radius: 36px;
  border: 3px solid rgba(255, 255, 255, 0.08);
  padding: 12px;
  box-shadow:
    0 40px 80px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
  animation: phoneFadeIn 1.2s cubic-bezier(0.22, 1, 0.36, 1) 0.6s both;
}
@keyframes phoneFadeIn {
  from { opacity: 0; transform: translateY(40px) rotateY(-8deg); }
  to { opacity: 1; transform: translateY(0) rotateY(0); }
}
.phone-screen {
  width: 100%;
  height: 100%;
  background: linear-gradient(170deg, #111827, #0f172a);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.mock-header {
  padding: 0;
}
.mock-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px 8px;
  font-size: 12px;
  font-weight: 600;
  color: #f8fafc;
}
.mock-icons {
  display: flex;
  gap: 4px;
}
.mock-icons span {
  display: block;
  width: 14px;
  height: 10px;
  background: #f8fafc;
  border-radius: 2px;
  opacity: 0.7;
}
.mock-app-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px 16px;
  font-size: 16px;
  font-weight: 600;
  font-family: var(--font-display);
  color: #f8fafc;
}
.mock-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
}
.mock-body {
  flex: 1;
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.mock-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  transition: all 0.3s;
}
.mock-card--active {
  background: rgba(6, 214, 160, 0.06);
  border-color: rgba(6, 214, 160, 0.2);
}
.mock-card-icon {
  font-size: 24px;
}
.mock-card-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}
.mock-card-text strong {
  font-size: 13px;
  color: #f1f5f9;
}
.mock-card-text span {
  font-size: 11px;
  color: #64748b;
}
.mock-badge-live {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #06d6a0;
  background: rgba(6, 214, 160, 0.12);
  padding: 4px 10px;
  border-radius: 999px;
  animation: pulse 2.5s ease-in-out infinite;
}

/* ─── FEATURES ─── */
.features {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 40px 48px 100px;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
.feature-card {
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  padding: 32px 28px;
  transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}
.feature-card:hover {
  transform: translateY(-6px);
  border-color: rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #fff;
  margin-bottom: 20px;
}
.feature-card h3 {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #f1f5f9;
}
.feature-card p {
  font-size: 14px;
  line-height: 1.65;
  color: #64748b;
}

/* ─── CTA BANNER ─── */
.cta-banner {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 48px 100px;
}
.cta-inner {
  background: linear-gradient(135deg, rgba(6, 214, 160, 0.08), rgba(131, 56, 236, 0.08));
  border: 1px solid rgba(6, 214, 160, 0.12);
  border-radius: 28px;
  padding: 64px;
  text-align: center;
}
.cta-inner h2 {
  font-family: var(--font-display);
  font-size: clamp(28px, 3.5vw, 42px);
  font-weight: 700;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
}
.cta-inner p {
  font-size: 16px;
  color: #94a3b8;
  margin-bottom: 36px;
  max-width: 520px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.65;
}

/* ─── FOOTER ─── */
.landing-footer {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 40px 48px;
  border-top: 1px solid var(--surface-border);
  color: #475569;
  font-size: 13px;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .landing-nav {
    padding: 20px 24px;
  }
  .hero {
    flex-direction: column;
    padding: 48px 24px 64px;
    text-align: center;
    gap: 48px;
  }
  .hero-content {
    max-width: 100%;
  }
  .hero-badge {
    font-size: 11px;
  }
  .hero-subtitle {
    max-width: 100%;
  }
  .hero-actions {
    justify-content: center;
  }
  .phone-mockup {
    width: 240px;
    height: 480px;
  }
  .features {
    padding: 20px 24px 64px;
  }
  .features-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .cta-banner {
    padding: 0 24px 64px;
  }
  .cta-inner {
    padding: 40px 24px;
    border-radius: 20px;
  }
  .landing-footer {
    padding: 32px 24px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 34px;
    letter-spacing: -1px;
  }
  .hero-subtitle {
    font-size: 15px;
  }
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  .btn-download, .btn-ghost {
    width: 100%;
    justify-content: center;
  }
  .phone-mockup {
    width: 220px;
    height: 440px;
  }
}
</style>
