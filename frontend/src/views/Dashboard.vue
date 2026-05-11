<template>
  <!-- Hidden print-only header that shows at the top of the printed page -->
  <div class="print-header">
    <h1>SOAVS — Election Results Report</h1>
    <p v-if="selectedElectionData">{{ selectedElectionData.election.title }}</p>
    <p class="print-date">Generated on {{ new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }}</p>
    <p v-if="selectedElectionData" class="print-status">Status: {{ selectedElectionData.election.calculated_status }}</p>
  </div>
  <div class="dashboard-container animation-fade-in">
    <div class="header">
      <div class="title-action-wrapper">
        <div>
          <h1>Election Dashboard</h1>
          <p>System Overview & Current Metrics</p>
        </div>
        <button class="btn-sync" @click="fetchStats" :disabled="loading">
          <span :class="{ 'spin': loading }">🔄</span> Sync Data
        </button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card glass-panel" v-for="(stat, index) in statItems" :key="index">
        <div class="stat-icon" :style="{ color: stat.color }">
          <i :class="stat.icon"></i>
        </div>
        <div class="stat-info">
          <div class="stat-title">{{ stat.title }}</div>
          <div class="stat-value" :class="{ 'loading-pulse': loading }">
            {{ loading ? '...' : stat.value }}
          </div>
        </div>
      </div>
    </div>

    <div class="main-content-grid">
      <div class="chart-container glass-panel">
        <div class="panel-header">
          <div style="display: flex; align-items: center; gap: 15px;">
            <h3>Election Results</h3>
            <select v-model="selectedElectionId" class="election-select input-glass" @change="fetchResults">
              <option disabled value="">Select an election</option>
              <option v-for="election in publishedElections" :key="election.id" :value="election.id">
                {{ election.title }}
              </option>
            </select>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <button
              v-if="selectedElectionData"
              class="btn-print"
              @click="handlePrintRequest"
              title="Print election results"
            >
              <i class="fas fa-print"></i> Print Results
            </button>
            <span v-if="selectedElectionData" class="badge" :class="selectedElectionData.election.calculated_status.toLowerCase()">
              {{ selectedElectionData.election.calculated_status }}
            </span>
          </div>
        </div>
        <div class="chart-content results-container">
          <p v-if="loadingResults" class="text-muted text-center" style="padding: 40px 0;">Loading results...</p>
          
          <div v-else-if="selectedElectionData && selectedElectionData.positions.length > 0" class="positions-list">
            <div v-for="pos in selectedElectionData.positions" :key="pos.id" class="position-result-group">
              <h4 class="position-title">{{ pos.name }}</h4>
              
              <div v-for="cand in pos.candidates" :key="cand.id" class="candidate-bar-row" :class="{ 'is-winner': isWinner(pos, cand) }">
                <div class="candidate-info">
                  <span class="cand-name">
                    <span v-if="isWinner(pos, cand)" class="winner-badge"><i class="fas fa-trophy"></i> Winner</span>
                    {{ cand.name }}
                  </span>
                  <span class="cand-votes">{{ cand.vote_count }} votes</span>
                </div>
                <div class="bar-bg">
                  <div class="bar-fill" :class="{ 'bar-fill-winner': isWinner(pos, cand) }" :style="{ width: calculateWidth(cand.vote_count) }"></div>
                </div>
              </div>
              
              <div v-if="pos.candidates.length === 0" class="text-muted" style="font-size: 13px; margin-top: 5px;">
                No candidates for this position.
              </div>
            </div>
          </div>
          
          <div v-else class="placeholder-chart">
            <div class="empty-state">
              <p>Select a published election to view real-time results.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="recent-activity-container glass-panel">
        <h3>System Activity</h3>
        <div v-if="loading" class="loading-activity">
          <div class="activity-skeleton" v-for="i in 3" :key="i"></div>
        </div>
        <ul v-else class="activity-list">
          <li v-if="stats.total_voters > 0">
            <span class="dot success"></span>
            Voter roster updated with {{ stats.total_voters }} eligible voters.
          </li>
          <li v-if="stats.active_elections > 0">
            <span class="dot primary"></span>
            {{ stats.active_elections }} election(s) currently accepting votes.
          </li>
          <li v-if="stats.total_votes > 0">
            <span class="dot warning"></span>
            Total of {{ stats.total_votes }} votes successfully recorded.
          </li>
          <li v-if="Object.values(stats).every(v => v === 0)" class="text-muted">
            No activity detected yet. Start by setting up an election.
          </li>
        </ul>
      </div>
    </div>

    <!-- Print Confirmation Dialog -->
    <ConfirmDialog
      :visible="showPrintConfirm"
      title="Election Still Ongoing"
      message="The election is still ongoing. Do you still want to continue?"
      subtitle="The printed results may not be final."
      confirmText="Yes, Print"
      cancelText="Cancel"
      variant="warning"
      @confirm="executePrint"
      @cancel="showPrintConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import axios from '../axios';
import ConfirmDialog from '../components/ConfirmDialog.vue';

const stats = ref({
  active_elections: 0,
  total_candidates: 0,
  total_voters: 0,
  total_votes: 0
});

const loading = ref(true);
const publishedElections = ref([]);
const selectedElectionId = ref("");
const selectedElectionData = ref(null);
const loadingResults = ref(false);
const showPrintConfirm = ref(false);
let refreshInterval = null;
let resultsInterval = null;

const statItems = computed(() => [
  { title: 'Active Elections', value: stats.value.active_elections, color: '#3b82f6', icon: 'fas fa-poll' },
  { title: 'Total Candidates', value: stats.value.total_candidates, color: '#10b981', icon: 'fas fa-user-tie' },
  { title: 'Total Voters', value: stats.value.total_voters?.toLocaleString(), color: '#8b5cf6', icon: 'fas fa-users' },
  { title: 'Votes Cast', value: stats.value.total_votes?.toLocaleString(), color: '#f59e0b', icon: 'fas fa-vote-yea' },
  { 
    title: 'Voter Turnout', 
    value: stats.value.total_voters > 0 
      ? `${((stats.value.total_votes / stats.value.total_voters) * 100).toFixed(1)}%` 
      : '0%', 
    color: '#ec4899', 
    icon: 'fas fa-chart-line' 
  }
]);

const fetchStats = async () => {
  try {
    loading.value = true;
    const response = await axios.get('dashboard-stats/');
    stats.value = response.data;
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error);
  } finally {
    loading.value = false;
  }
};

const fetchPublishedElections = async () => {
  try {
    const response = await axios.get('elections/');
    // Filter out draft elections
    publishedElections.value = response.data.filter(e => e.status !== 'DRAFT');
    
    // Auto-select the first active election if none is selected
    if (!selectedElectionId.value && publishedElections.value.length > 0) {
      const active = publishedElections.value.find(e => e.calculated_status === 'ACTIVE' || e.status === 'ACTIVE');
      selectedElectionId.value = active ? active.id : publishedElections.value[0].id;
      fetchResults();
    }
  } catch (error) {
    console.error('Failed to fetch published elections:', error);
  }
};

const fetchResults = async () => {
  if (!selectedElectionId.value) return;
  try {
    if (!selectedElectionData.value) loadingResults.value = true; // only show loading indicator on first load
    const response = await axios.get(`elections/${selectedElectionId.value}/results/`);
    selectedElectionData.value = response.data;
  } catch (error) {
    console.error('Failed to fetch election results:', error);
  } finally {
    loadingResults.value = false;
  }
};

const calculateWidth = (votes) => {
  if (votes === 0) return '0%';
  const total = stats.value.total_voters > 0 ? stats.value.total_voters : 1;
  return `${(votes / total) * 100}%`;
};

// --- Print Results Logic ---
const isWinner = (position, candidate) => {
  // Only highlight winners when the election is completed
  if (!selectedElectionData.value) return false;
  const status = selectedElectionData.value.election.calculated_status;
  if (status !== 'COMPLETED') return false;

  if (!position.candidates || position.candidates.length === 0) return false;
  const maxVotes = Math.max(...position.candidates.map(c => c.vote_count));
  if (maxVotes === 0) return false;
  return candidate.vote_count === maxVotes;
};

const handlePrintRequest = () => {
  if (!selectedElectionData.value) return;
  const status = selectedElectionData.value.election.calculated_status;
  if (status === 'ACTIVE' || status === 'UPCOMING') {
    showPrintConfirm.value = true;
  } else {
    executePrint();
  }
};

const executePrint = () => {
  showPrintConfirm.value = false;
  nextTick(() => {
    window.print();
  });
};

onMounted(() => {
  fetchStats();
  fetchPublishedElections();
  
  // Auto-refresh stats every 60 seconds
  refreshInterval = setInterval(() => {
      fetchStats();
      fetchPublishedElections();
  }, 60000);

  // Auto-refresh results every 15 seconds
  resultsInterval = setInterval(() => {
      if (selectedElectionId.value) {
          fetchResults();
      }
  }, 15000);
});

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
  if (resultsInterval) clearInterval(resultsInterval);
});
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}
.header {
  margin-bottom: 30px;
}
.header h1 {
  font-size: 32px;
  font-weight: 800;
  background: linear-gradient(to right, #fff, #94a3b8);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 5px;
}
.header p {
  color: #94a3b8;
  font-size: 16px;
}
.title-action-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.btn-sync {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 14px;
}
.btn-sync:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.2);
}
.btn-sync:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.spin {
  display: inline-block;
  animation: rotate 2s linear infinite;
}
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s ease, border-color 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-5px);
  border-color: rgba(255, 255, 255, 0.2);
}
.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}
.stat-title {
  font-size: 13px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  margin-bottom: 4px;
}
.stat-value {
  font-size: 28px;
  font-weight: 800;
}
.main-content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 25px;
}
@media (max-width: 1024px) {
  .main-content-grid {
      grid-template-columns: 1fr;
  }
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.badge {
  background: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}
.badge.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}
.badge.completed {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}
.badge.upcoming {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}
.placeholder-chart {
  height: 300px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.empty-state {
  text-align: center;
  color: #64748b;
  max-width: 300px;
}
.activity-list {
  list-style: none;
  padding: 0;
}
.activity-list li {
  padding: 15px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot.primary { background: #3b82f6; }
.dot.success { background: #10b981; }
.dot.warning { background: #f59e0b; }

.loading-pulse {
  animation: pulse 1.5s infinite;
  color: #334155;
}
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Results Styles */
.results-container {
    max-height: 400px;
    overflow-y: auto;
    padding-right: 10px;
}
.positions-list {
    display: flex;
    flex-direction: column;
    gap: 25px;
}
.position-result-group {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 8px;
    padding: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
.position-title {
    font-size: 16px;
    color: var(--primary-color);
    margin-bottom: 15px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 8px;
}
.candidate-bar-row {
    margin-bottom: 15px;
}
.candidate-bar-row:last-child {
    margin-bottom: 0;
}
.candidate-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 14px;
}
.cand-name {
    color: #e2e8f0;
    font-weight: 500;
}
.cand-votes {
    color: #94a3b8;
    font-size: 13px;
}
.bar-bg {
    width: 100%;
    height: 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    background: linear-gradient(to right, #3b82f6, #60a5fa);
    border-radius: 6px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.election-select {
    background: rgba(15, 23, 42, 0.6);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 14px;
    min-width: 200px;
    outline: none;
}
.election-select:focus {
    border-color: var(--primary-color);
}

.animation-fade-in {
  animation: fadeIn 0.6s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Print Button */
.btn-print {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.25);
  color: #10b981;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s;
}
.btn-print:hover {
  background: rgba(16, 185, 129, 0.2);
  border-color: #10b981;
  transform: translateY(-1px);
}

/* Winner Highlight */
.is-winner {
  background: rgba(245, 158, 11, 0.06);
  border-left: 3px solid #f59e0b;
  padding-left: 12px;
  border-radius: 4px;
}
.winner-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
  margin-right: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.winner-badge i {
  font-size: 10px;
}
.bar-fill-winner {
  background: linear-gradient(to right, #f59e0b, #fbbf24) !important;
}

/* Print-only header (hidden on screen) */
.print-header {
  display: none;
}

/* ===== Print Styles ===== */
@media print {
  /* Show the print header */
  .print-header {
    display: block !important;
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 16px;
    border-bottom: 2px solid #000;
  }
  .print-header h1 {
    font-size: 24px;
    font-weight: 800;
    color: #000 !important;
    background: none !important;
    -webkit-text-fill-color: #000 !important;
    margin-bottom: 6px;
  }
  .print-header p {
    color: #333 !important;
    font-size: 12px;
    margin: 2px 0;
  }
  .print-header .print-status {
    font-weight: 700;
    text-transform: uppercase;
    font-size: 13px;
    margin-top: 4px;
  }

  /* Reset page */
  * {
    color: #000 !important;
    background: transparent !important;
    box-shadow: none !important;
    text-shadow: none !important;
  }
  body {
    background: #fff !important;
    color: #000 !important;
    font-family: 'Times New Roman', Times, serif !important;
    font-size: 12pt;
  }

  /* Hide ALL non-essential UI */
  .sidebar,
  .header,
  .stats-grid,
  .recent-activity-container,
  .panel-header,
  .btn-sync,
  .btn-print,
  .election-select,
  .modal-overlay,
  .badge {
    display: none !important;
  }

  /* Hide the progress bars entirely */
  .bar-bg {
    display: none !important;
  }

  /* Reset layout — no sidebar margin */
  .has-sidebar .main-content {
    margin-left: 0 !important;
    padding: 0 !important;
  }
  .dashboard-container {
    padding: 10px !important;
  }
  .main-content-grid {
    display: block !important;
  }

  /* Strip glass panel styling */
  .chart-container.glass-panel {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
  }
  .results-container {
    max-height: none !important;
    overflow: visible !important;
    padding: 0 !important;
  }
  .positions-list {
    gap: 0 !important;
  }

  /* Position groups — clean bordered sections */
  .position-result-group {
    background: none !important;
    border: none !important;
    border-bottom: 1px solid #999 !important;
    border-radius: 0 !important;
    padding: 12px 0 !important;
    margin-bottom: 0 !important;
    page-break-inside: avoid;
  }
  .position-title {
    color: #000 !important;
    font-size: 14pt !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px;
    border-bottom: none !important;
    padding-bottom: 4px !important;
    margin-bottom: 8px !important;
  }

  /* Candidate rows — simple text lines */
  .candidate-bar-row {
    margin-bottom: 4px !important;
    padding: 4px 0 !important;
    border-left: none !important;
    background: none !important;
    border-radius: 0 !important;
    padding-left: 16px !important;
  }
  .candidate-info {
    font-size: 12pt !important;
    margin-bottom: 0 !important;
  }
  .cand-name {
    color: #000 !important;
    font-weight: 400 !important;
    font-size: 12pt !important;
  }
  .cand-votes {
    color: #000 !important;
    font-size: 12pt !important;
    font-weight: 600 !important;
  }

  /* Winner row — bold with clear label */
  .is-winner {
    background: none !important;
    border-left: none !important;
    padding-left: 16px !important;
  }
  .is-winner .cand-name {
    font-weight: 700 !important;
  }
  .is-winner .cand-votes {
    font-weight: 800 !important;
  }
  .winner-badge {
    background: none !important;
    color: #000 !important;
    font-size: 10pt !important;
    font-weight: 800 !important;
    padding: 0 !important;
    margin-right: 6px !important;
    border-radius: 0 !important;
    border: 1px solid #000 !important;
    padding: 1px 6px !important;
  }
  .winner-badge i {
    display: none !important;
  }
}
</style>
