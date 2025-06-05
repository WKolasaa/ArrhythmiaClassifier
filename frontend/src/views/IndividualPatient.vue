<template>
  <q-page padding>
    <q-card class="q-pa-md">
      <q-card-section>
        <div class="text-h6">Patient Information</div>
      </q-card-section>

      <q-card-section v-if="patient">
        <q-list>
          <q-item>
            <q-item-section><strong>Name:</strong> {{ patient.name }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Birth Date:</strong> {{ patient.birth_date }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Gender:</strong> {{ patient.gender }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Contact Info:</strong> {{ patient.contact_info }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Created At:</strong> {{ patient.created_at }}</q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-section v-else>
        <q-spinner size="lg" color="primary" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePatientStore } from "@/stores/patients";

const route = useRoute();
const patient = ref(null);

const store = usePatientStore();

onMounted(async () => {
  store.fetchPatientDetails()
});
</script>