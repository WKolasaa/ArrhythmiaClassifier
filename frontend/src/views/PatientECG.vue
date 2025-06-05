<template>
  <q-page padding>
    <q-card class="q-pa-md">
      <q-card-section>
        <div class="text-h6">ECG Visualization - Heartbeat #{{ heartbeat?.id }}</div>
        <div class="text-subtitle2">Predicted: {{ heartbeat?.predicted_type }} (Confidence: {{ confidence }})</div>
      </q-card-section>

      <q-card-section>
        <canvas ref="ecgChart" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import Chart from 'chart.js/auto';
import { usePatientStore } from '@/stores/pacient';

const route = useRoute();
const store = usePatientStore();
const ecgChart = ref(null);
const heartbeat = ref(null);
const patientId = route.params.patientId;
const heartbeatId = route.params.heartbeatId;

const confidence = computed(() =>
  heartbeat.value?.prediction_confidence ? `${(heartbeat.value.prediction_confidence * 100).toFixed(1)}%` : '--'
);

onMounted(async () => {
  heartbeat.value = await store.fetchHeartbeatById(patientId, heartbeatId);
  drawChart();
});

function drawChart() {
  if (!heartbeat.value || !ecgChart.value) return;

  const peaks = [
    { label: 'P', value: heartbeat.value.p_peak },
    { label: 'Q', value: heartbeat.value.q_peak },
    { label: 'R', value: heartbeat.value.r_peak },
    { label: 'S', value: heartbeat.value.s_peak },
    { label: 'T', value: heartbeat.value.t_peak },
  ];

  const labels = peaks.map(p => p.label);
  const data = peaks.map(p => p.value);

  new Chart(ecgChart.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'ECG Peaks',
          data,
          fill: false,
          tension: 0.3,
          borderColor: '#1976D2',
          pointBackgroundColor: '#E53935',
          pointRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
        },
      },
    },
  });
}
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 300px;
}
</style>