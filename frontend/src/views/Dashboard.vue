<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md q-mb-md">
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Total Patients</div>
          <div class="text-h4">{{ patientStore.all.length }}</div>
        </q-card-section>
      </q-card>
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">New Patients</div>
          <div class="text-h4">--</div>
        </q-card-section>
      </q-card>
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Classified Arrhythmias</div>
          <div class="text-h4">--</div>
        </q-card-section>
      </q-card>
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Total Arrhythmias</div>
          <div class="text-h4">--</div>
        </q-card-section>
      </q-card>
    </div>

    <q-card flat bordered class="q-pa-md">
      <q-card-section class="text-h6 text-primary">
        Patient List
      </q-card-section>
      <q-table
        :rows="patientStore.all"
        :columns="columns"
        row-key="id"
        flat
        bordered
        dense
        no-data-label="No patients found"
      />
    </q-card>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { usePatientStore } from '../stores/pacient'


const patientStore = usePatientStore()

onMounted(() => {
  patientStore.fetchAllPatients()
})

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' },
  { name: 'name', label: 'Name', field: 'name', align: 'left' },
  { name: 'gender', label: 'Gender', field: 'gender', align: 'left' },
  { name: 'birth_date', label: 'Birth Date', field: 'birth_date', align: 'left' },
  { name: 'contact_info', label: 'Contact Info', field: 'contact_info', align: 'left' }
]
</script>

<style scoped> 
:deep(.q-card.bg-white) {
  background-color: var(--q-color-surface) !important;
  color: var(--q-color-on-surface) !important;
}
</style>
