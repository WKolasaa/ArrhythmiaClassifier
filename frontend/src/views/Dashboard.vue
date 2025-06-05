<template>
  <q-page class="q-pa-md">
    <!-- Info Cards -->
    <div class="row q-col-gutter-md q-mb-md">
      <q-card class="col" flat bordered :dark="$q.dark.isActive">
        <q-card-section>
          <div class="text-h6">Total Patients</div>
          <div class="text-h4">{{ totalPatients }}</div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Patient List -->
    <q-card flat bordered class="q-pa-md">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6 text-primary col">Patient List</div>
        <q-space />
        <q-btn color="primary" label="New Patient" @click="showDialog = true" />
      </q-card-section>
      <q-table class="q-mt-md" :rows="patients" :columns="columns" row-key="id" flat bordered dense />
    </q-card>

    <!-- CSV Upload Button -->
    <div class="q-mt-md" style="max-width: 100%">
      <q-btn class="full-width" color="primary" icon="upload" label="Import CSV File" @click="showUploadDialog = true" />
    </div>

    <!-- Add Patient Dialog -->
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

    <!-- Import CSV Dialog -->
    <q-dialog v-model="showUploadDialog">
      <q-card class="full-width" style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Import Heartbeat CSV</div>
        </q-card-section>

        <q-card-section>
          <q-select v-model="selectedModel" label="Select Model" :options="modelOptions" outlined dense class="q-mb-sm" />
          <q-file v-model="csvFile" label="Select CSV File" accept=".csv" outlined dense counter use-chips class="full-width" />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn :disable="isUploading" flat label="Upload" color="primary" @click="handleFileUpload" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue'
import { usePatientStore } from '../stores/pacient'

const { proxy } = getCurrentInstance()

const showDialog = ref(false)
const showUploadDialog = ref(false)
const isUploading = ref(false)

const csvFile = ref(null)
const selectedModel = ref(null)
const modelOptions = ref([])

const patientStore = usePatientStore()
const patients = ref([])

const newPatient = ref({
  name: '',
  gender: '',
  birth_date: '',
  contact_info: ''
})

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

const fetchPatients = async () => {
  await patientStore.fetchAllPatients()
  patients.value = patientStore.all
}

const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:5001/patients/stats', {
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      }
    })
    const data = await response.json()
    if (response.ok) {
      totalPatients.value = data.total_patients
      classified.value = data.classified_arrhythmias
      totalArrhythmias.value = data.total_arrhythmias
    } else {
      proxy?.$q?.notify?.({ type: 'negative', message: data.error || 'Failed to load stats' })
    }
  } catch (err) {
    proxy?.$q?.notify?.({ type: 'negative', message: 'Stats fetch error: ' + err.message })
  }
}

const submitPatient = async () => {
  if (!newPatient.value.name) {
    proxy?.$q?.notify?.({ type: 'warning', message: 'Name is required' })
    return
  }

  try {
    await patientStore.createPatient(newPatient.value)
    await fetchPatients()
    await fetchStats()
    showDialog.value = false
    newPatient.value = { name: '', gender: '', birth_date: '', contact_info: '' }
    proxy?.$q?.notify?.({ type: 'positive', message: 'Patient created successfully', timeout: 2000 })
  } catch (err) {
    proxy?.$q?.notify?.({ type: 'negative', message: 'Failed to create patient.' })
  }
}

const fetchModelOptions = async () => {
  try {
    const response = await fetch('http://localhost:5001/model/models', {
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      }
    })
    const data = await response.json()
    if (response.ok) {
      modelOptions.value = data.models
    } else {
      proxy?.$q?.notify?.({ type: 'negative', message: data.error || 'Failed to fetch model list' })
    }
  } catch (err) {
    proxy?.$q?.notify?.({ type: 'negative', message: 'Model list error: ' + err.message })
  }
}

const handleFileUpload = async () => {
  if (!csvFile.value || !selectedModel.value) {
    proxy?.$q?.notify?.({ type: 'warning', message: 'Please select both model and CSV file.' })
    return
  }

  const formData = new FormData()
  formData.append('file', csvFile.value)
  formData.append('model_name', selectedModel.value)

  isUploading.value = true
  showUploadDialog.value = false
  proxy?.$q?.loading.show({ message: 'Uploading and predicting...' })

  try {
    const response = await fetch('http://localhost:5001/model/predict', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      },
      body: formData
    })

    const result = await response.json()

    if (response.ok) {
      proxy?.$q?.notify?.({ type: 'positive', message: result.message || 'Prediction successful' })
      await fetchPatients()
      await fetchStats()
    } else {
      proxy?.$q?.notify?.({ type: 'negative', message: result.error || 'Prediction failed' })
    }
  } catch (err) {
    proxy?.$q?.notify?.({ type: 'negative', message: 'Upload error: ' + err.message })
  } finally {
    isUploading.value = false
    proxy?.$q?.loading.hide()
    csvFile.value = null
    selectedModel.value = null
  }
}

onMounted(() => {
  fetchPatients()
  fetchModelOptions()
  fetchStats()
})
</script>
