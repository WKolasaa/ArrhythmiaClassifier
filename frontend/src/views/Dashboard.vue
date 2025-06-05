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
      <q-card class="col" flat bordered :dark="$q.dark.isActive">
        <q-card-section>
          <div class="text-h6">New Patients</div>
          <div class="text-h4">{{ newPatients }}</div>
        </q-card-section>
      </q-card>
      <q-card class="col" flat bordered :dark="$q.dark.isActive">
        <q-card-section>
          <div class="text-h6">Classified Arrhythmias</div>
          <div class="text-h4">{{ classified }}</div>
        </q-card-section>
      </q-card>
      <q-card class="col" flat bordered :dark="$q.dark.isActive">
        <q-card-section>
          <div class="text-h6">Total Arrhythmias</div>
          <div class="text-h4">{{ totalArrhythmias }}</div>
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

    <!-- CSV Upload Button Outside -->
    <div class="q-mt-md" style="max-width: 100%">
      <q-btn class="full-width" color="primary" icon="upload" label="Import CSV File"
        @click="showUploadDialog = true" />
    </div>
    <!-- Add Patient Dialog -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Add New Patient</div>
        </q-card-section>

        <q-card-section>
          <q-input v-model="newPatient.name" label="Name" outlined dense />
          <q-select v-model="newPatient.gender" label="Gender" outlined dense :options="['Male', 'Female', 'Other']"
            class="q-mt-sm" />
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
      <q-card class="full-width">
        <q-card-section>
          <div class="text-h6">Import Heartbeat CSV</div>
        </q-card-section>

        <q-card-section>
          <q-file v-model="csvFile" label="Select CSV File" accept=".csv" outlined dense counter use-chips
            class="full-width" />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Upload" color="primary" @click="handleFileUpload" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePatientStore } from '../stores/pacient'

const patientStore = usePatientStore()
const showDialog = ref(false)
const showUploadDialog = ref(false)
const csvFile = ref(null)

const totalPatients = ref(218)
const newPatients = ref(125)
const classified = ref(25)
const totalArrhythmias = ref(2479)

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' },
  { name: 'name', label: 'Name', field: 'name', align: 'left' },
  { name: 'gender', label: 'Gender', field: 'gender', align: 'left' },
  { name: 'birth_date', label: 'Birth Date', field: 'birth_date', align: 'left' },
  { name: 'contact_info', label: 'Contact Info', field: 'contact_info', align: 'left' }
]

const patients = ref([])
const newPatient = ref({
  name: '',
  gender: '',
  birth_date: '',
  contact_info: ''
})

const fetchPatients = async () => {
  await patientStore.fetchAllPatients()
  patients.value = patientStore.all
}

const submitPatient = async () => {
  if (!newPatient.value.name) {
    alert('Name is required')
    return
  }

  try {
    await patientStore.createPatient(newPatient.value)
    await fetchPatients()
    showDialog.value = false
    newPatient.value = { name: '', gender: '', birth_date: '', contact_info: '' }
  } catch (err) {
    alert('Failed to create patient.')
  }
}

const handleFileUpload = () => {
  if (!csvFile.value) {
    alert('Please select a CSV file.')
    return
  }

  // Placeholder logic
  console.log('Uploading file:', csvFile.value.name)

  showUploadDialog.value = false
  csvFile.value = null
}

onMounted(() => {
  fetchPatients()
})
</script>
