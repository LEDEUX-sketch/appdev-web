<template>
  <div class="elections-container animation-fade-in">
    <div class="header-action-wrapper">
      <div>
        <h1>Election Configurations</h1>
        <p class="text-muted">Set up active election cycles and ballot positions</p>
      </div>
      <div>
        <button class="btn-primary" @click="openCreateModal">+ New Election</button>
      </div>
    </div>

    <div v-for="election in elections" :key="election.id" class="glass-panel election-card">
      <div class="election-info">
        <div class="election-header">
          <h2>{{ election.title }}</h2>
          <span class="status-badge" :class="(election.calculated_status || election.status || 'draft').toLowerCase()">
            {{ election.calculated_status || election.status }}
          </span>
        </div>
        <div class="election-details">
          <p><strong>Starts:</strong> {{ election.start_date ? new Date(election.start_date).toLocaleString() : 'Not set' }}</p>
          <p><strong>Ends:</strong> {{ election.end_date ? new Date(election.end_date).toLocaleString() : 'Not set' }}</p>
        </div>
      </div>
      <div class="election-actions">
        <button class="btn-primary-sm" @click="openPositionModal(election)">Manage Positions</button>
        <button class="btn-text-sm" @click="openEditModal(election)">Edit Details</button>
        <button class="btn-text-sm text-danger" @click="deleteElection(election.id)">Delete</button>
      </div>
    </div>

    <div v-if="elections.length === 0" class="glass-panel text-center empty-state">
      <h3>No elections defined</h3>
      <p class="text-muted">Create an election to begin setting up positions and candidates.</p>
    </div>

    <!-- Election Modal (Create/Edit) -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content glass-panel">
        <h2>{{ isEditing ? 'Edit Election' : 'Create New Election' }}</h2>
        <form @submit.prevent="saveElection">
          <div class="form-group">
            <label>Election Title</label>
            <input v-model="newElection.title" type="text" class="input-glass" placeholder="e.g. Supreme Student Council 2026" required />
          </div>
          <div class="form-group">
            <label>Start Date & Time</label>
            <input v-model="newElection.start_date" type="datetime-local" class="input-glass" required />
          </div>
          <div class="form-group">
            <label>End Date & Time</label>
            <input v-model="newElection.end_date" type="datetime-local" class="input-glass" required />
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="newElection.status" class="input-glass">
              <option value="DRAFT">DRAFT</option>
              <option value="ACTIVE">ACTIVE</option>
              <option value="COMPLETED">COMPLETED</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showModal = false">Cancel</button>
            <button type="submit" class="btn-primary" :disabled="submitting">
              {{ submitting ? 'Saving...' : (isEditing ? 'Update Election' : 'Create Election') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Manage Positions Modal -->
    <div v-if="showPositionModal" class="modal-overlay" @click.self="showPositionModal = false">
      <div class="modal-content glass-panel" style="max-width: 600px;">
        <div class="modal-header">
          <h2>Positions for {{ selectedElection?.title }}</h2>
          <button class="close-btn" @click="showPositionModal = false">&times;</button>
        </div>
        
        <div class="position-list-section">
          <div v-if="positions.length === 0" class="text-muted text-center" style="padding: 20px;">
            No positions added yet.
          </div>
          <div v-else class="position-items">
            <div v-for="pos in positions" :key="pos.id" class="position-item glass-panel">
              <div class="pos-info">
                <strong>{{ pos.name }}</strong>
                <span>(Max votes: {{ pos.max_votes_allowed }})</span>
              </div>
              <button class="btn-icon-danger" @click="deletePosition(pos.id)">🗑️</button>
            </div>
          </div>
        </div>

        <div class="add-position-section">
          <h3>Add New Position</h3>
          <form @submit.prevent="createPosition" class="inline-form">
            <input v-model="newPosition.name" type="text" class="input-glass" placeholder="Position Name (e.g. President)" required />
            <input v-model.number="newPosition.max_votes_allowed" type="number" class="input-glass" style="width: 80px;" placeholder="Max" title="Max Votes" required />
            <button type="submit" class="btn-primary" :disabled="submittingPosition">+</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../axios'

const elections = ref([])
const positions = ref([])
const showModal = ref(false)
const showPositionModal = ref(false)
const isEditing = ref(false)
const selectedElection = ref(null)
const submitting = ref(false)
const submittingPosition = ref(false)
let refreshInterval = null

const newElection = ref({
    title: '',
    start_date: '',
    end_date: '',
    status: 'DRAFT'
})

const newPosition = ref({
    name: '',
    max_votes_allowed: 1,
    hierarchy_order: 0
})

const fetchElections = async () => {
    try {
        const response = await api.get('elections/')
        elections.value = response.data
    } catch (error) {
        console.error('Error fetching elections:', error)
    }
}

const openCreateModal = () => {
    resetForm()
    showModal.value = true
}

const openEditModal = (election) => {
    isEditing.value = true
    selectedElection.value = election
    
    // Convert to local datetime string for input (YYYY-MM-DDThh:mm)
    const start = new Date(election.start_date)
    const end = new Date(election.end_date)
    
    const toLocalISO = (date) => {
        if (!date || isNaN(date.getTime())) return ''
        const pad = (num) => String(num).padStart(2, '0')
        return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
    }

    newElection.value = {
        title: election.title,
        start_date: toLocalISO(start),
        end_date: toLocalISO(end),
        status: election.status || 'DRAFT'
    }
    showModal.value = true
}

const resetForm = () => {
    isEditing.value = false
    selectedElection.value = null
    newElection.value = { title: '', start_date: '', end_date: '', status: 'DRAFT' }
}

const openPositionModal = async (election) => {
    selectedElection.value = election
    showPositionModal.value = true
    fetchPositionsForElection(election.id)
}

const fetchPositionsForElection = async (electionId) => {
    try {
        const response = await api.get(`positions/?election=${electionId}`)
        positions.value = response.data.filter(p => p.election === electionId)
    } catch (error) {
        console.error('Error fetching positions:', error)
    }
}

const createPosition = async () => {
    try {
        submittingPosition.value = true
        const data = {
            ...newPosition.value,
            election: selectedElection.value.id
        }
        await api.post('positions/', data)
        newPosition.value = { name: '', max_votes_allowed: 1, hierarchy_order: 0 }
        fetchPositionsForElection(selectedElection.value.id)
    } catch (error) {
        console.error('Error creating position:', error)
    } finally {
        submittingPosition.value = false
    }
}

const deletePosition = async (id) => {
    if (!confirm('Are you sure you want to delete this position?')) return
    try {
        await api.delete(`positions/${id}/`)
        fetchPositionsForElection(selectedElection.value.id)
    } catch (error) {
        console.error('Error deleting position:', error)
    }
}

const deleteElection = async (id) => {
    if (!confirm('Are you sure you want to delete this election? All related positions and candidates will be affected.')) return
    try {
        await api.delete(`elections/${id}/`)
        fetchElections()
    } catch (error) {
        console.error('Error deleting election:', error)
        alert('Failed to delete election.')
    }
}

const saveElection = async () => {
    try {
        submitting.value = true
        if (isEditing.value) {
            await api.put(`elections/${selectedElection.value.id}/`, newElection.value)
        } else {
            await api.post('elections/', newElection.value)
        }
        showModal.value = false
        resetForm()
        fetchElections()
    } catch (error) {
        console.error('Error saving election:', error)
        alert('Failed to save election. Check your input.')
    } finally {
        submitting.value = false
    }
}

onMounted(() => {
    fetchElections()
    // Auto-refresh every 60 seconds
    refreshInterval = setInterval(fetchElections, 60000)
})

onUnmounted(() => {
    if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<style scoped>
.elections-container {
    padding: 10px;
}
.header-action-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}
.text-muted {
    color: #94a3b8;
}
.election-card {
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.election-info {
    flex: 1;
}
.election-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 10px;
}
.election-header h2 {
    font-size: 20px;
    color: var(--primary-color);
    margin: 0;
}
.status-badge {
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
}
.status-badge.draft {
    background: rgba(148, 163, 184, 0.2);
    color: #94a3b8;
}
.status-badge.upcoming {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
}
.status-badge.active {
    background: rgba(16, 185, 129, 0.2);
    color: var(--success-color);
}
.status-badge.completed {
    background: rgba(59, 130, 246, 0.2);
    color: var(--primary-color);
}
.election-details p {
    margin-bottom: 4px;
    font-size: 14px;
    color: #94a3b8;
}
.election-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding-left: 20px;
    border-left: 1px solid var(--glass-border);
}
.btn-primary-sm {
    background: var(--primary-color);
    color: white;
    font-size: 13px;
    padding: 8px 12px;
}
.btn-text-sm {
    background: transparent;
    color: #94a3b8;
    font-size: 12px;
    padding: 4px;
}
.btn-text-sm:hover {
    color: white;
}

/* Position Modal Styles */
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.close-btn {
    background: transparent;
    font-size: 24px;
    color: #94a3b8;
    padding: 0;
}
.position-items {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
    max-height: 250px;
    overflow-y: auto;
}
.position-item {
    padding: 12px 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.03);
}
.pos-info span {
    margin-left: 10px;
    font-size: 13px;
    color: #64748b;
}
.btn-icon-danger {
    background: transparent;
    padding: 5px;
    opacity: 0.6;
}
.btn-icon-danger:hover {
    opacity: 1;
}
.add-position-section {
    padding-top: 20px;
    border-top: 1px solid var(--glass-border);
}
.add-position-section h3 {
    font-size: 16px;
    margin-bottom: 15px;
}
.inline-form {
    display: flex;
    gap: 10px;
}
.text-center {
    text-align: center;
}
.empty-state {
    padding: 60px;
}
</style>
