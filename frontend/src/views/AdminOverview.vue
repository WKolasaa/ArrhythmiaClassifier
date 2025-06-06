<template>
  <q-page class="q-pa-md">
    <!-- Metric Cards -->
    <div class="row q-gutter-sm q-mb-md justify-around">
      <q-card
        v-for="metric in metrics"
        :key="metric.label"
        class="col-2 q-pa-md"
        flat
        bordered
        :class="metricCardClass"
      >
        <q-card-section class="text-center">
          <q-icon :name="metric.icon" size="36px" class="q-mb-sm" />
          <div class="text-subtitle2">{{ metric.label }}</div>
          <div class="text-h5 q-mt-xs">{{ metric.value }}</div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Class Distribution & Per-Class Performance -->
    <div class="row q-col-gutter-md q-mb-md">
      <q-card class="col-6" flat bordered>
        <q-card-section class="text-h6">Class Distribution</q-card-section>
        <q-card-section>
          <BarChart
            :chartData="classDistributionData"
            :chartOptions="chartOptions"
          />
        </q-card-section>
      </q-card>

      <q-card class="col-6" flat bordered>
        <q-card-section class="text-h6">Pre-Class Performance</q-card-section>
        <q-card-section>
          <q-markup-table dense flat bordered>
            <thead>
              <tr>
                <th>Class</th>
                <th>F1 Score</th>
                <th>Precision</th>
                <th>Recall</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in classMetrics" :key="row.class">
                <td>{{ row.class }}</td>
                <td>{{ row.f1 }}</td>
                <td>{{ row.precision }}</td>
                <td>{{ row.recall }}</td>
              </tr>
            </tbody>
          </q-markup-table>
        </q-card-section>
      </q-card>
    </div>

    <!-- Confusion Matrix -->
    <q-card flat bordered class="q-pa-md">
      <q-card-section class="text-h6">Confusion Matrix</q-card-section>
      <q-card-section class="confusion-matrix">
        <div class="matrix-container">
          <!-- Top row: empty corner + Predicted label -->
          <div class="cell corner"></div>
          <div class="cell span-columns" :colspan="labels.length"></div>

          <!-- Header row: blank + predicted class labels -->
          <div class="cell header">Actual | Predicted</div>
          <div
            v-for="label in labels"
            :key="'pred-label-' + label"
            class="cell header"
          >
            {{ label }}
          </div>

          <!-- Matrix rows -->
          <template v-for="(row, rowIndex) in matrix" :key="'row-' + rowIndex">
            <div class="cell header">{{ labels[rowIndex] }}</div>
            <div
              v-for="(value, colIndex) in row"
              :key="'val-' + rowIndex + '-' + colIndex"
              class="cell"
              :style="{ backgroundColor: colors[colIndex % colors.length] }"
            >
              {{ value }}
            </div>
          </template>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, computed } from "vue";
import { Dark } from "quasar";
import BarChart from "../components/BarChart.vue";

const isDark = computed(() => Dark.isActive);
const metricCardClass = computed(() =>
  isDark.value ? "bg-dark text-white" : "bg-white text-primary"
);

const metrics = ref([
  { label: "Accuracy", value: "0.95", icon: "check_circle" },
  { label: "Precision", value: "0.92", icon: "precision_manufacturing" },
  { label: "Recall", value: "0.90", icon: "history" },
  { label: "F1-score", value: "0.91", icon: "equalizer" },
]);

const classDistributionData = {
  labels: ["Normal", "AFib", "PVC", "LBBB"],
  datasets: [
    {
      label: "Count",
      backgroundColor: ["#42A5F5", "#66BB6A", "#FFA726", "#AB47BC"],
      data: [4700, 1100, 1000, 900],
    },
  ],
};

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: true },
  },
  scales: {
    y: {
      beginAtZero: true,
    },
  },
};

const classMetrics = ref([
  { class: "Normal", f1: "0.96", precision: "0.92", recall: "0.95" },
  { class: "AFib", f1: "0.86", precision: "0.86", recall: "0.83" },
  { class: "PVC", f1: "0.90", precision: "0.90", recall: "0.80" },
  { class: "LBBB", f1: "0.90", precision: "0.90", recall: "0.90" },
]);

const labels = ["Normal", "AFib", "PVC"];
const matrix = [
  [95, 2, 1],
  [41, 8, 1],
  [2, 47, 5],
];
const colors = ["#42A5F5", "#66BB6A", "#FFA726"];
</script>

<style scoped>
.confusion-matrix .matrix-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Adjust if you add more classes */
  grid-auto-rows: minmax(30px, auto);
  text-align: center;
  gap: 2px;
}

.cell {
  padding: 8px;
  border: 1px solid #ccc;
  font-weight: bold;
  color: white;
}

.cell.header {
  background-color: #333;
  color: white;
}

.cell.corner {
  grid-column: span 1;
  background-color: transparent;
  border: none;
}

.cell.span-columns {
  grid-column: span 3;
  font-weight: bold;
  color: black;
  background-color: transparent;
  border: none;
  text-align: center;
}
</style>
