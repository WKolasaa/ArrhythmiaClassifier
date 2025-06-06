<template>
  <q-page padding>
    <!-- Summary Cards -->
    <div class="row q-col-gutter-md q-mb-md">
      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Total Heartbeats</div>
          <div class="text-h4">{{ statusData?.total_heartbeats ?? "--" }}</div>
        </q-card-section>
      </q-card>

      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Abnormal Heartbeats</div>
          <div class="text-h4">
            {{ statusData?.abnormal_heartbeats ?? "--" }}
          </div>
        </q-card-section>
      </q-card>

      <q-card class="col bg-white text-primary" flat bordered>
        <q-card-section>
          <div class="text-h6">Status</div>
          <div class="text-h4 text-uppercase">
            {{ statusData?.status ?? "--" }}
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Patient Details Table -->
    <q-card class="q-pa-sm q-mb-md">
      <q-card-section>
        <div class="text-h6">Patient Information</div>
        <q-markup-table flat bordered class="q-mt-sm table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Birth Date</th>
              <th>Gender</th>
              <th>Contact Info</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody class="table">
            <tr>
              <td>{{ name }}</td>
              <td>{{ birth_date }}</td>
              <td>{{ gender }}</td>
              <td>{{ contact_info }}</td>
              <td>{{ created_at }}</td>
            </tr>
          </tbody>
        </q-markup-table>
      </q-card-section>
    </q-card>

    <!-- Heartbeats Table -->
    <q-card>
      <q-card-section>
        <div class="text-h6">Heartbeats</div>
        <q-table
          :rows="heartbeats"
          :columns="columns"
          row-key="id"
          flat
          bordered
          class="table"
        >
          <template v-slot:body-cell-actions="props">
            <q-td align="center">
              <q-btn
                color="primary"
                label="See ECG"
                size="md"
                @click="goToEcg(props.row.id)"
              />
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { usePatientStore } from "@/stores/patients";

const route = useRoute();
const router = useRouter();
const patient = ref(null);
const patientId = route.params.id;

const store = usePatientStore();

onMounted(async () => {
  await store.fetchPatientDetails(patientId);
  await store.fetchPatientStatus(patientId);
  await store.fetchPatientHeartbeats(patientId);
});

const name = computed(() => store.selectedPatient?.name || "");
const birth_date = computed(() => store.selectedPatient?.birth_date || "");
const contact_info = computed(() => store.selectedPatient?.contact_info || "");
const created_at = computed(() => store.selectedPatient?.created_at || "");
const gender = computed(() => store.selectedPatient?.gender || "");

const statusData = computed(() => store.status);
const heartbeats = computed(() => store.heartbeats);

const columns = [
  { name: "id", label: "ID", field: "id", sortable: true },
  { name: "heartbeat_type", label: "Heartbeat Type", field: "heartbeat_type" },
  { name: "predicted_type", label: "Prediction", field: "predicted_type" },
  { name: "timestamp", label: "Timestamp", field: "timestamp" },
  { name: "actions", label: "Actions", field: "actions", sortable: false },
];

function goToEcg(heartbeatId) {
  router.push(`/patients/${patientId}/heartbeats/${heartbeatId}`);
}
</script>

<style scooped>
.table th {
  font-weight: bold;
  font-size: 16px;
  text-align: center;
}

.table tbody td {
  font-size: 16px;
  text-align: center;
}
</style>
