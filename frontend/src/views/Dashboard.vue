<template>
  <q-page class="q-pa-md">
    <!-- Dashboard cards -->    <!-- DASHBOARD TITLE -->
    <div class="text-h5 text-weight-bold q-mb-md q-ml-sm">Dashboard</div>

    <!-- DASHBOARD CARDS -->
    <div class="row q-gutter-md q-mb-xl">
      <q-card
        flat
        bordered
        class="dashboard-card q-pa-md col-12 col-sm-6 col-md-3"
        v-for="card in cards"
        :key="card.label"
        style="min-height: 120px;"
      >
        <q-card-section class="q-pa-sm">
          <div class="row items-center justify-between">
            <div class="column">
              <div class="text-subtitle2 text-grey-7">{{ card.label }}</div>
              <div class="text-h6 text-bold text-primary">{{ card.value }}</div>
            </div>
            <q-icon :name="card.icon" :color="card.color" size="32px" />
          </div>
          <q-linear-progress :value="card.progress" :color="card.color" class="q-mt-sm" rounded />
        </q-card-section>
      </q-card>
    </div>

    <!-- Patient List & Actions -->
    <q-card flat bordered class="q-pa-md">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6 text-primary col">Patient List</div>
        <q-space />
        <div class="row q-gutter-sm">
          <q-btn color="primary" label="New Patient" icon="person_add" @click="showDialog = true" />
          <q-btn color="primary" label="Upload & Analyze Heartbeat" icon="upload" @click="showUploadDialog = true" />
          <q-btn color="secondary" label="Bulk Add Patients" icon="group_add" @click="showBulkUploadDialog = true" />
        </div>
      </q-card-section>

      <q-table
        class="q-mt-md"
        :rows="patients"
        :columns="columns"
        row-key="id"
        flat
        bordered
        dense
        @row-click="goToPatient"
      />
    </q-card>

    <!-- New Patient Dialog -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Add New Patient</div>
        </q-card-section>
        <q-card-section>
          <q-input v-model="newPatient.name" label="Name" outlined dense />
          <q-select v-model="newPatient.gender" label="Gender" outlined dense :options="['Male', 'Female', 'Other']" class="q-mt-sm" />
          <q-input v-model="newPatient.birth_date" label="Birth Date" type="date" outlined dense class="q-mt-sm" />
          <q-input v-model="newPatient.contact_info" label="Contact Info" outlined dense class="q-mt-sm" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Save" color="primary" @click="submitPatient" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Import Heartbeat CSV Dialog -->
    <q-dialog v-model="showUploadDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Import Heartbeat CSV</div>
        </q-card-section>
        <q-card-section>
          <q-select v-model="selectedModel" label="Select Model" :options="modelOptions" outlined dense class="q-mb-sm" />
          <q-file v-model="csvFile" label="Select CSV File" accept=".csv" outlined dense use-chips counter />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn :disable="isUploading" flat label="Upload" color="primary" @click="handleFileUpload" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Bulk Upload Patients Dialog -->
    <q-dialog v-model="showBulkUploadDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Bulk Add Patients</div>
        </q-card-section>
        <q-card-section>
          <q-file v-model="bulkPatientCsv" label="Select CSV File" accept=".csv" outlined dense use-chips counter />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn :disable="isUploading" flat label="Upload" color="secondary" @click="handleBulkPatientUpload" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>


<script setup>
import { ref, onMounted, getCurrentInstance, computed } from 'vue'
import { usePatientStore } from '@/stores/patients'
import { useRouter } from 'vue-router'

const { proxy } = getCurrentInstance()
const router = useRouter()

const showDialog = ref(false)
const showUploadDialog = ref(false)
const showBulkUploadDialog = ref(false)

const isUploading = ref(false)
const patients = ref([])
const modelOptions = ref([])

const csvFile = ref(null)
const bulkPatientCsv = ref(null)
const selectedModel = ref(null)

const patientStore = usePatientStore()

const newPatient = ref({ name: '', gender: '', birth_date: '', contact_info: '' })
const totalPatients = ref(0)
const classified = ref(0)
const totalArrhythmias = ref(0)

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' },
  { name: 'name', label: 'Name', field: 'name', align: 'left' },
  { name: 'gender', label: 'Gender', field: 'gender', align: 'left' },
  { name: 'birth_date', label: 'Birth Date', field: 'birth_date', align: 'left' },
  { name: 'contact_info', label: 'Contact Info', field: 'contact_info', align: 'left' },
  { name: 'last_prediction', label: 'Prediction', field: 'last_prediction', align: 'left' }
]

const cards = computed(() => [
  {
    label: 'New Patients',
    value: '125', // Replace with real value if needed
    icon: 'person_add',
    color: 'purple',
    progress: 0.5
  },
  {
    label: 'Total Patients',
    value: totalPatients.value,
    icon: 'groups',
    color: 'blue',
    progress: 1
  },
  {
    label: 'Classified Arrhythmias',
    value: classified.value,
    icon: 'favorite',
    color: 'green',
    progress: 0.4
  },
  {
    label: 'Total Arrhythmias',
    value: totalArrhythmias.value,
    icon: 'monitor_heart',
    color: 'orange',
    progress: 0.7
  }
])


const fetchPatients = async () => {
  await patientStore.fetchAllPatients()
  patients.value = patientStore.all
}

const fetchStats = async () => {
  try {
    const res = await fetch('http://localhost:5001/patients/stats', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const data = await res.json()
    if (res.ok) {
      totalPatients.value = data.total_patients
      classified.value = data.classified_arrhythmias
      totalArrhythmias.value = data.total_arrhythmias
    }
  } catch (err) {
    proxy?.$q?.notify({ type: 'negative', message: 'Failed to fetch stats: ' + err.message })
  }
}

const submitPatient = async () => {
  if (!newPatient.value.name) {
    proxy?.$q?.notify({ type: 'warning', message: 'Name is required' })
    return
  }
  try {
    await patientStore.createPatient(newPatient.value)
    await fetchPatients()
    await fetchStats()
    showDialog.value = false
    proxy?.$q?.notify({ type: 'positive', message: 'Patient created' })
  } catch (err) {
    proxy?.$q?.notify({ type: 'negative', message: 'Creation failed' })
  }
}

const fetchModelOptions = async () => {
  try {
    const res = await fetch('http://localhost:5001/model/models', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const data = await res.json()
    if (res.ok) {
      modelOptions.value = data.models
    }
  } catch (err) {
    proxy?.$q?.notify({ type: 'negative', message: 'Model fetch failed' })
  }
}

const handleFileUpload = async () => {
  if (!csvFile.value || !selectedModel.value) {
    proxy?.$q?.notify({ type: 'warning', message: 'Select model and file' })
    return
  }

  const formData = new FormData()
  formData.append('file', csvFile.value)
  formData.append('model_name', selectedModel.value)

  isUploading.value = true
  showUploadDialog.value = false
  proxy?.$q?.loading.show({ message: 'Analyzing...' })

  try {
    const res = await fetch('http://localhost:5001/model/predict', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') },
      body: formData
    })
    const result = await res.json()
    if (res.ok) {
      proxy?.$q?.notify({ type: 'positive', message: result.message || 'Success' })
      await fetchPatients()
      await fetchStats()
    } else {
      proxy?.$q?.notify({ type: 'negative', message: result.error || 'Failed' })
    }
  } catch (err) {
    proxy?.$q?.notify({ type: 'negative', message: 'Error: ' + err.message })
  } finally {
    isUploading.value = false
    proxy?.$q?.loading.hide()
    csvFile.value = null
    selectedModel.value = null
  }
}

const handleBulkPatientUpload = async () => {
  if (!bulkPatientCsv.value) {
    proxy?.$q?.notify({ type: 'warning', message: 'Select a CSV file' })
    return
  }

  const formData = new FormData()
  formData.append('file', bulkPatientCsv.value)

  isUploading.value = true
  showBulkUploadDialog.value = false
  proxy?.$q?.loading.show({ message: 'Uploading bulk patients...' })

  try {
    const res = await fetch('http://localhost:5001/patients/bulk-upload', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') },
      body: formData
    })
    const data = await res.json()
    if (res.ok) {
      proxy?.$q?.notify({ type: 'positive', message: data.message || 'Uploaded' })
      await fetchPatients()
    } else {
      proxy?.$q?.notify({ type: 'negative', message: data.error || 'Upload failed' })
    }
  } catch (err) {
    proxy?.$q?.notify({ type: 'negative', message: 'Bulk upload error: ' + err.message })
  } finally {
    isUploading.value = false
    proxy?.$q?.loading.hide()
    bulkPatientCsv.value = null
  }
}

function goToPatient(evt, row) {
  router.push(`/patients/${row.id}`)
}

onMounted(() => {
  fetchPatients()
  fetchModelOptions()
  fetchStats()
})
</script>

<style scoped>
.dashboard-cards-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
  padding: 0 24px;
}

.dashboard-card {
  flex: 1 1 220px;
  max-width: 800px;
  min-width: 220px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
</style>
