<template>
  <div class="candidates-container animation-fade-in">
    <div class="header-action-wrapper">
      <div>
        <h1>Candidate Manager</h1>
        <p class="text-muted">Manage candidates, platforms, and partylists</p>
      </div>
      <div>
        <button class="btn-primary" @click="openCreateModal">+ Add Candidate</button>
      </div>
    </div>

    <div class="candidates-grid">
      <div v-for="candidate in candidates" :key="candidate.id" class="glass-panel candidate-card">
        <div class="candidate-header">
          <div class="avatar-placeholder">
            <span v-if="!candidate.photo">{{ candidate.name.charAt(0) }}</span>
            <img v-else :src="candidate.photo" :alt="candidate.name" class="candidate-img" />
          </div>
          <div class="candidate-info">
            <h3>{{ candidate.name }}</h3>
            <p class="position-badge">{{ candidate.position_name || 'No Position' }}</p>
          </div>
        </div>
        <div class="candidate-body">
          <p><strong>Party:</strong> {{ candidate.partylist_name || 'Independent' }}</p>
          <p><strong>Course:</strong> {{ candidate.course_and_year || 'N/A' }}</p>
          <p class="platform-text">"{{ candidate.platform_statement || 'No platform stated.' }}"</p>
        </div>
        <div class="candidate-actions">
          <button class="btn-text" @click="openEditModal(candidate)">Edit</button>
          <button class="btn-text text-danger" @click="promptDeleteCandidate(candidate)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="candidates.length === 0" class="glass-panel text-center empty-state">
      <h3>No candidates available</h3>
      <p class="text-muted">Add your first candidate to populate the ballot.</p>
    </div>

    <!-- Add/Edit Candidate Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content glass-panel">
        <h2>{{ isEditing ? 'Edit Candidate' : 'Add New Candidate' }}</h2>
        <form @submit.prevent="saveCandidate">
          <div class="form-group">
            <label>Full Name</label>
            <input v-model="newCandidate.name" type="text" class="input-glass" required />
          </div>
          <div class="form-group">
            <label>Position</label>
            <select v-model="newCandidate.position" class="input-glass" required>
              <option value="" disabled>Select Position</option>
              <option v-for="pos in positions" :key="pos.id" :value="pos.id">{{ pos.name }} ({{ pos.election_title }})</option>
            </select>
          </div>
          <div class="form-group">
            <label>Partylist</label>
            <select v-model="newCandidate.partylist" class="input-glass">
              <option :value="null">Independent</option>
              <option v-for="party in partylists" :key="party.id" :value="party.id">{{ party.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Course & Year</label>
            <input v-model="newCandidate.course_and_year" type="text" class="input-glass" placeholder="e.g. BSCS 4A" />
          </div>
          <div class="form-group">
            <label>Platform Statement</label>
            <textarea v-model="newCandidate.platform_statement" class="input-glass" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Photo</label>
            <input type="file" @change="handleFileUpload" accept="image/*" class="input-glass" />
            <p v-if="isEditing && candidate.photo" class="text-muted" style="font-size: 11px; margin-top: 5px;">
              Leave blank to keep existing photo.
            </p>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showModal = false">Cancel</button>
            <button type="submit" class="btn-primary" :disabled="submitting">
              {{ submitting ? 'Saving...' : (isEditing ? 'Save Changes' : 'Add Candidate') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Candidate Confirmation -->
    <ConfirmDialog
      :visible="showDeleteDialog"
      title="Delete Candidate"
      :message="`Are you sure you want to delete ${candidateToDelete?.name}?`"
      subtitle="This will permanently remove the candidate and their associated votes."
      confirmText="Yes, Delete"
      variant="danger"
      @confirm="confirmDeleteCandidate"
      @cancel="showDeleteDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const candidates = ref([])
const positions = ref([])
const partylists = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const selectedCandidate = ref(null)
const submitting = ref(false)
const showDeleteDialog = ref(false)
const candidateToDelete = ref(null)

const newCandidate = ref({
    name: '',
    position: '',
    partylist: null,
    course_and_year: '',
    platform_statement: '',
    photo: null
})

const handleFileUpload = (event) => {
    newCandidate.value.photo = event.target.files[0]
}

const fetchCandidates = async () => {
    try {
        const response = await api.get('candidates/')
        candidates.value = response.data
    } catch (error) {
        console.error('Error fetching candidates:', error)
    }
}

const openCreateModal = () => {
    isEditing.value = false
    selectedCandidate.value = null
    newCandidate.value = { name: '', position: '', partylist: null, course_and_year: '', platform_statement: '' }
    showModal.value = true
}

const openEditModal = (candidate) => {
    isEditing.value = true
    selectedCandidate.value = candidate
    newCandidate.value = {
        name: candidate.name,
        position: candidate.position,
        partylist: candidate.partylist,
        course_and_year: candidate.course_and_year,
        platform_statement: candidate.platform_statement
    }
    showModal.value = true
}

const fetchFormData = async () => {
    try {
        const [posRes, partyRes] = await Promise.all([
            api.get('positions/'),
            api.get('partylists/')
        ])
        positions.value = posRes.data
        partylists.value = partyRes.data
    } catch (error) {
        console.error('Error fetching form data:', error)
    }
}

const saveCandidate = async () => {
    try {
        submitting.value = true
        
        const formData = new FormData()
        formData.append('name', newCandidate.value.name)
        formData.append('position', newCandidate.value.position)
        if (newCandidate.value.partylist) formData.append('partylist', newCandidate.value.partylist)
        formData.append('course_and_year', newCandidate.value.course_and_year)
        formData.append('platform_statement', newCandidate.value.platform_statement)
        
        if (newCandidate.value.photo) {
            formData.append('photo', newCandidate.value.photo)
        }

        const config = {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }

        if (isEditing.value) {
            await api.patch(`candidates/${selectedCandidate.value.id}/`, formData, config)
        } else {
            await api.post('candidates/', formData, config)
        }
        showModal.value = false
        fetchCandidates()
    } catch (error) {
        console.error('Error saving candidate:', error)
        alert('Failed to save candidate. Please verify all required fields.')
    } finally {
        submitting.value = false
    }
}

const promptDeleteCandidate = (candidate) => {
    candidateToDelete.value = candidate
    showDeleteDialog.value = true
}

const confirmDeleteCandidate = async () => {
    if (!candidateToDelete.value) return
    try {
        await api.delete(`candidates/${candidateToDelete.value.id}/`)
        showDeleteDialog.value = false
        candidateToDelete.value = null
        fetchCandidates()
    } catch (error) {
        console.error('Error deleting candidate:', error)
        alert('Failed to delete candidate.')
    }
}

onMounted(() => {
    fetchCandidates()
    fetchFormData()
})
</script>

<style scoped>
.candidates-container {
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
.candidates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}
.candidate-card {
    display: flex;
    flex-direction: column;
}
.candidate-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 15px;
}
.avatar-placeholder {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(59, 130, 246, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    color: var(--primary-color);
    overflow: hidden;
}
.candidate-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.candidate-info h3 {
    margin: 0 0 5px 0;
    font-size: 18px;
}
.position-badge {
    display: inline-block;
    padding: 2px 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    font-size: 12px;
    color: #cbd5e1;
}
.candidate-body {
    flex: 1;
    font-size: 14px;
}
.candidate-body p {
    margin-bottom: 8px;
}
.platform-text {
    font-style: italic;
    color: #94a3b8;
    margin-top: 15px;
}
.candidate-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid var(--glass-border);
}
.btn-text {
    background: transparent;
    color: var(--primary-color);
    padding: 5px 10px;
}
.btn-text:hover {
    background: rgba(255, 255, 255, 0.05);
}
.text-danger {
    color: var(--danger-color);
}
.text-center {
    text-align: center;
}
.empty-state {
    padding: 60px;
}
</style>
