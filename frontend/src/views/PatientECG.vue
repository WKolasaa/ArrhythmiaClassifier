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
import { useRoute} from 'vue-router';
import Chart from 'chart.js/auto';
import { usePatientStore } from '@/stores/patients';

const route = useRoute();
const store = usePatientStore();
const ecgChart = ref(null);
const heartbeat = ref(null);
const patientId = route.params.id;
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

  const samplingRate = 360; // Hz
  const msToSamples = ms => Math.max(Math.floor((ms / 1000) * samplingRate), 1);

  const p = heartbeat.value.p_peak;
  const q = heartbeat.value.q_peak;
  const r = heartbeat.value.r_peak;
  const s = heartbeat.value.s_peak;
  const t = heartbeat.value.t_peak;

  const pq_int = msToSamples(heartbeat.value.pq_interval);
  const qrs_int = msToSamples(heartbeat.value.qrs_interval);
  const qt_int = msToSamples(heartbeat.value.qt_interval);

  const pPos = Math.floor(pq_int / 3);
  const qPos = pq_int - 1;
  const rPos = pq_int + Math.floor(qrs_int / 3);
  const sPos = pq_int + qrs_int - 1;
  const tPos = pq_int + qrs_int + Math.floor(qt_int / 2);

  const x = Array.from({ length: pq_int + qrs_int + qt_int }, (_, i) => i);
  const y = [
    ...interpolate(0, p, pPos),
    ...interpolate(p, q, qPos - pPos),
    ...interpolate(q, r, rPos - qPos),
    ...interpolate(r, s, sPos - rPos),
    ...interpolate(s, t, tPos - sPos),
    ...interpolate(t, 0, x.length - tPos)
  ];

  const peakIndexes = [pPos, qPos, rPos, sPos, tPos];
  const peakValues = [p, q, r, s, t];
  const peakLabels = ['P', 'Q', 'R', 'S', 'T'];

  new Chart(ecgChart.value, {
    type: 'line',
    data: {
      labels: x.slice(0, y.length),
      datasets: [
        {
          label: 'ECG Waveform',
          data: y,
          fill: false,
          tension: 0.3,
          borderColor: '#1976D2',
          pointRadius: 0,
        },
        {
          label: 'Peaks',
          data: peakIndexes.map((i, idx) => ({ x: i, y: peakValues[idx], label: peakLabels[idx] })),
          showLine: false,
          pointBackgroundColor: '#E53935',
          pointRadius: 6,
          pointHoverRadius: 7,
        }
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: 'Amplitude (mV)'
          }
        },
        x: {
          display: false
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              const point = context.raw;
              return `Peak: ${point.label}, Value: ${point.y.toFixed(3)}`;
            }
          }
        }
      }
    },
  });
}

function interpolate(start, end, steps) {
  const stepSize = (end - start) / steps;
  return Array.from({ length: steps }, (_, i) => start + i * stepSize);
}
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 300px;
}
</style>
