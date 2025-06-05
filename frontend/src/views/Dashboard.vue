<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md q-mb-md">
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Total Patients</div>
          <div class="text-h4">{{ totalPatients }}</div>
        </q-card-section>
      </q-card>
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">New Patients</div>
          <div class="text-h4">{{ newPatients }}</div>
        </q-card-section>
      </q-card>
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Classified Arrhythmias</div>
          <div class="text-h4">{{ classified }}</div>
        </q-card-section>
      </q-card>
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Total Arrhythmias</div>
          <div class="text-h4">{{ totalArrhythmias }}</div>
        </q-card-section>
      </q-card>
    </div>

    <q-card flat bordered class="q-pa-md">
      <q-card-section class="text-h6 text-primary">
        Patient List
      </q-card-section>
      <q-table
        :rows="patients"
        :columns="columns"
        row-key="id"
        flat
        bordered
        dense
      />
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'

const totalPatients = ref(218)
const newPatients = ref(125)
const classified = ref(25)
const totalArrhythmias = ref(2479)

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' },
  { name: 'name', label: 'Name', field: 'name', align: 'left' },
  { name: 'doctor', label: 'Assigned Doctor', field: 'doctor', align: 'left' },
  { name: 'admitDate', label: 'Date of Admit', field: 'admitDate', align: 'left' },
  { name: 'disease', label: 'Condition', field: 'disease', align: 'left' },
  { name: 'room', label: 'Room No', field: 'room', align: 'left' }
]

const patients = ref([
  { id: 1, name: 'Jens Brincker', doctor: 'Dr. Kenny', admitDate: '2023-05-27', disease: 'Bradycardia', room: '101' },
  { id: 2, name: 'Mark Hay', doctor: 'Dr. Mark', admitDate: '2023-06-10', disease: 'Tachycardia', room: '102' },
  { id: 3, name: 'Anthony Davie', doctor: 'Dr. Cinnamon', admitDate: '2023-06-15', disease: 'AFib', room: '103' },
  { id: 4, name: 'David Perry', doctor: 'Dr. Felix', admitDate: '2023-06-22', disease: 'PVCs', room: '104' },
  { id: 5, name: 'Sue Woodger', doctor: 'Dr. Sharma', admitDate: '2023-07-01', disease: 'NSR', room: '105' }
])
</script>
