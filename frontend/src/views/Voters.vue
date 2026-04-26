<template>
  <div class="voters-container animation-fade-in">
    <div class="header-action-wrapper">
      <div>
        <h1>Voter Roll Manager</h1>
        <p class="text-muted">Upload and manage eligible student voters</p>
      </div>
      <div style="display: flex; gap: 10px;">
        <button class="btn-primary" @click="fetchVoters" :disabled="loading" style="background: rgba(59, 130, 246, 0.1); border-color: var(--primary-color); color: var(--primary-color);">
          🔄 Refresh
        </button>
        <button v-if="voters.length > 0" class="btn-primary" @click="printCards" style="background: rgba(16, 185, 129, 0.2); border-color: var(--success-color); color: var(--success-color);">
          🖨️ Print Voter Cards
        </button>
        <button v-if="voters.length > 0" class="btn-primary btn-danger-outline" @click="clearAllVoters">
          Remove All Voters
        </button>
        <input type="file" ref="fileInput" @change="handleFileUpload" accept=".csv" style="display:none" />
        <button class="btn-primary" @click="triggerFileInput">+ Upload CSV</button>
      </div>
    </div>

    <div class="glass-panel table-container">
      <div v-if="uploadMsg" class="upload-feedback" :class="{'success': isUploadSuccess, 'error': !isUploadSuccess}">
        {{ uploadMsg }}
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>Student ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="voter in voters" :key="voter.id">
            <td>{{ voter.student_id }}</td>
            <td>{{ voter.name }}</td>
            <td>{{ voter.email }}</td>
            <td>
              <span class="badge" :class="voter.has_voted ? 'badge-success' : 'badge-warning'">
                {{ voter.has_voted ? 'Voted' : 'Pending' }}
              </span>
            </td>
            <td>
              <button class="btn-icon-danger" @click="deleteVoter(voter.id)">🗑️</button>
            </td>
          </tr>
          <tr v-if="voters.length === 0">
            <td colspan="5" class="text-center">No voters found. Upload a CSV to get started.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Printable Voter Cards (Hidden by default, shown only in print) -->
    <div id="printable-cards" class="print-only">
      <div class="voter-cards-grid">
        <div v-for="voter in voters" :key="voter.id" class="voter-card">
          <div class="card-title">SOAVS Voter Card</div>
          <div class="card-detail"><strong>Name:</strong> {{ voter.name }}</div>
          <div class="card-detail"><strong>Student ID:</strong> {{ voter.student_id }}</div>
          <div class="card-detail token-detail"><strong>Token:</strong> {{ voter.unique_voting_token }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../axios'

const voters = ref([])
const fileInput = ref(null)
const uploadMsg = ref('')
const isUploadSuccess = ref(true)
const loading = ref(false)

let refreshInterval = null

const fetchVoters = async () => {
    try {
        loading.value = true
        const response = await api.get('voters/')
        voters.value = response.data
    } catch (error) {
        console.error('Error fetching voters:', error)
    } finally {
        loading.value = false
    }
}

const triggerFileInput = () => {
    fileInput.value.click()
}

const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
        const response = await api.post('voters/import/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        isUploadSuccess.value = true
        uploadMsg.value = response.data.success || 'Upload successful!'
        fetchVoters()
    } catch (error) {
        isUploadSuccess.value = false
        uploadMsg.value = error.response?.data?.error || 'Failed to upload CSV'
    }
    
    setTimeout(() => { uploadMsg.value = ''; }, 5000)
    event.target.value = null
}

const deleteVoter = async (id) => {
    if (!confirm('Are you sure you want to delete this voter?')) return
    try {
        await api.delete(`voters/${id}/`)
        fetchVoters()
    } catch (error) {
        console.error('Error deleting voter:', error)
        alert('Failed to delete voter.')
    }
}

const clearAllVoters = async () => {
    if (!confirm(`Are you sure you want to remove ALL ${voters.value.length} voter(s)? This cannot be undone.`)) return
    if (!confirm('This will permanently delete all voter records. Are you absolutely sure?')) return
    try {
        const response = await api.delete('voters/clear_all/')
        isUploadSuccess.value = true
        uploadMsg.value = response.data.success || 'All voters removed.'
        fetchVoters()
    } catch (error) {
        isUploadSuccess.value = false
        uploadMsg.value = error.response?.data?.error || 'Failed to remove voters.'
        console.error('Error clearing voters:', error)
    }
    setTimeout(() => { uploadMsg.value = ''; }, 5000)
}

const printCards = () => {
    window.print()
}

onMounted(() => {
    fetchVoters()
    refreshInterval = setInterval(fetchVoters, 30000)
})

onUnmounted(() => {
    if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<style>
@media print {
    body * {
        visibility: hidden;
    }
    #printable-cards, #printable-cards * {
        visibility: visible;
    }
    #printable-cards {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        display: block !important;
    }
    .voter-cards-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
    .voter-card {
        border: 2px dashed #000;
        padding: 20px;
        page-break-inside: avoid;
        font-family: monospace;
        color: #000 !important;
        background: #fff !important;
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        color: #000 !important;
    }
    .card-detail {
        font-size: 14px;
        margin-bottom: 8px;
        color: #000 !important;
    }
    .token-detail {
        font-size: 16px;
        margin-top: 15px;
        padding: 8px;
        border: 1px solid #000;
        text-align: center;
        background: #f9f9f9 !important;
    }
}
</style>

<style scoped>
.print-only {
    display: none;
}
.voters-container {
    padding: 10px;
}
.header-action-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}
.header-action-wrapper h1 {
    font-size: 28px;
}
.text-muted {
    color: #94a3b8;
}
.table-container {
    overflow-x: auto;
}
.data-table {
    width: 100%;
    border-collapse: collapse;
}
.data-table th, .data-table td {
    padding: 14px 16px;
    text-align: left;
    border-bottom: 1px solid var(--glass-border);
}
.data-table th {
    color: #cbd5e1;
    font-weight: 600;
    font-size: 14px;
    text-transform: uppercase;
}
.data-table tbody tr:hover {
    background: rgba(255, 255, 255, 0.02);
}
.text-center {
    text-align: center;
    padding: 40px !important;
    color: #64748b;
}
.badge {
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}
.badge-success {
    background: rgba(16, 185, 129, 0.2);
    color: var(--success-color);
}
.badge-warning {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
}
.upload-feedback {
    padding: 12px;
    margin-bottom: 20px;
    border-radius: 8px;
    font-weight: 500;
}
.upload-feedback.success {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
    border: 1px solid var(--success-color);
}
.upload-feedback.error {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger-color);
    border: 1px solid var(--danger-color);
}

.btn-icon-danger {
    background: transparent;
    padding: 5px;
    opacity: 0.6;
    font-size: 16px;
}
.btn-icon-danger:hover {
    opacity: 1;
}
.btn-danger-outline {
    background: rgba(239, 68, 68, 0.1) !important;
    border-color: var(--danger-color) !important;
    color: var(--danger-color) !important;
}
.btn-danger-outline:hover {
    background: rgba(239, 68, 68, 0.25) !important;
}
</style>
