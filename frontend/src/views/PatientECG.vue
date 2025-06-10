<template>
  <q-page padding>
    <q-btn
      label="Patient View"
      icon="arrow_back"
      color="primary"
      flat
      class="q-mb-lg"
      @click="$router.push('/patients/' + patientId)"
    />

    <q-card class="q-pa-md">
      <q-card-section>
        <div class="text-h6">ECG Visualization - Heartbeat #{{ heartbeat?.id }}</div>
        <div class="text-subtitle2">
          Predicted: {{ heartbeat?.predicted_type }} (Confidence: {{ confidence }})
        </div>
      </q-card-section>

      <q-card-section>
        <canvas ref="ecgChart" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import Chart from "chart.js/auto";
import { usePatientStore } from "@/stores/patients";

const route = useRoute();
const store = usePatientStore();
const ecgChart = ref(null);
const heartbeat = ref(null);
const patientId = route.params.id;
const heartbeatId = route.params.heartbeatId;

const confidence = computed(() =>
  heartbeat.value?.prediction_confidence
    ? `${(heartbeat.value.prediction_confidence * 100).toFixed(1)}%`
    : "--"
);

onMounted(async () => {
  heartbeat.value = await store.fetchHeartbeatById(patientId, heartbeatId);
  drawChart();
});

function drawChart() {
  if (!heartbeat.value || !ecgChart.value || !heartbeat.value.ecg_features) return;

  const samplingRate = 360; // Hz
  const sampleIntervalMs = 1000 / samplingRate; // Time per sample in ms (≈2.78 ms)

  // Filter out trailing zeros to avoid plotting flat segments
  const voltages = heartbeat.value.ecg_features.filter(v => v !== 0);
  if (voltages.length === 0) return; // Avoid plotting empty data

  // Generate time points (x-axis) in milliseconds
  const timePoints = voltages.map((_, i) => (i * sampleIntervalMs).toFixed(2));

  new Chart(ecgChart.value, {
    type: "line",
    data: {
      labels: timePoints,
      datasets: [
        {
          label: "ECG Waveform",
          data: voltages,
          fill: false,
          tension: 0.3,
          borderColor: "#1976D2",
          pointRadius: 0,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: "Amplitude (mV)",
          },
        },
        x: {
          title: {
            display: true,
            text: "Time (ms)",
          },
          ticks: {
            maxTicksLimit: 10, // Limit ticks for readability
          },
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              return `Amplitude: ${context.parsed.y.toFixed(3)} mV`;
            },
          },
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