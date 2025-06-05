<template>
  <q-page padding>
    <q-card class="q-pa-md">
      <q-card-section>
        <div class="text-h6">Patient Information</div>
      </q-card-section>

      <q-card-section>
        <q-list>
          <q-item>
            <q-item-section><strong>Name:</strong> {{ name }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Birth Date:</strong> {{ birth_date }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Gender:</strong> {{ gender }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Contact Info:</strong> {{ contact_info }}</q-item-section>
          </q-item>
          <q-item>
            <q-item-section><strong>Created At:</strong> {{ created_at }}</q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <!-- <q-card-section v-else>
        <q-spinner size="lg" color="primary" />
      </q-card-section> -->
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePatientStore } from "@/stores/pacient";

const route = useRoute();
const patient = ref(null);
const patientId = route.params.id;

const store = usePatientStore();

onMounted(async () => {
  store.fetchPatientDetails(patientId);
});

const name = computed(() => store.selectedPatient?.name || "");
const birth_date = computed(() => store.selectedPatient?.birth_date || "");
const contact_info = computed(() => store.selectedPatient?.contact_info || "");
const created_at = computed(() => store.selectedPatient?.created_at || "");
const gender = computed(() => store.selectedPatient?.gender || "");
</script>