<template>
  <q-page padding class="bg-grey-2">
    <q-card flat bordered class="q-pa-md">
      <!-- Header -->
      <q-card-section class="text-h6 text-primary q-pb-md">
        Model Performance Records
      </q-card-section>

      <!-- Table Section -->
      <q-card-section class="q-pa-none">
        <div class="scrollable-table-container">
          <q-markup-table flat bordered dense class="striped-table bg-white">
            <thead class="bg-primary text-white">
              <tr>
                <th class="text-left">Model Name</th>
                <th class="text-center">Accuracy</th>
                <th class="text-center">Timestamp</th>
                <th class="text-center">Confusion Matrix</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="model in performanceList" :key="model.id" class="hoverable-row">
                <td class="text-left text-body1 q-px-sm q-py-xs">
                  {{ model.model_name }}
                </td>
                <td class="text-center text-body1 q-px-sm q-py-xs">
                  {{ model.accuracy?.toFixed(4) || '—' }}
                </td>
                <td class="text-center text-body1 q-px-sm q-py-xs">
                  {{ formatTimestamp(model.timestamp) }}
                </td>
                <td class="text-center q-px-sm q-py-xs">
                  <div class="nested-matrix-container">
                    <q-markup-table dense bordered flat class="bg-grey-1 nested-matrix-table">
                      <thead>
                        <tr>
                          <th></th>
                          <th
                            v-for="(label, i) in classLabels"
                            :key="'header-' + i"
                            class="text-center text-caption"
                          >
                            {{ label }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(row, rowIndex) in model.confusion_matrix"
                          :key="'row-' + rowIndex"
                        >
                          <td class="text-left text-caption text-bold q-pl-sm">
                            {{ classLabels[rowIndex] }}
                          </td>
                          <td
                            v-for="(cell, colIndex) in row"
                            :key="'cell-' + colIndex"
                            class="text-center text-caption nested-cell"
                            :class="rowIndex === colIndex ? 'bg-green-2 text-bold' : ''"
                          >
                            {{ cell }}
                          </td>
                        </tr>
                      </tbody>
                    </q-markup-table>
                  </div>
                </td>
              </tr>
            </tbody>
          </q-markup-table>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const performanceList = ref([])

const classLabels = [
  'Normal',
  'Supraventricular',
  'Premature',
  'Arrhythmic',
  'Unknown'
]

const fetchModelPerformances = async () => {
  try {
    const res = await fetch('http://localhost:5001/model/model-performance', {
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      }
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to fetch performance list')

    const allDetails = await Promise.all(
      data.accuracies.map(async (entry) => {
        const detailRes = await fetch(
          `http://localhost:5001/model/model-performance/${entry.id}`,
          {
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem('token')
            }
          }
        )
        return await detailRes.json()
      })
    )

    performanceList.value = allDetails
  } catch (err) {
    console.error('Error loading model performance records:', err.message)
  }
}

const formatTimestamp = (ts) => {
  if (!ts) return '—'
  const date = new Date(ts)
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(fetchModelPerformances)
</script>

<style scoped>
/* Make the page background a very light grey */
.bg-grey-2 {
  background-color: #f5f5f5;
}

/* Header styling */
.text-primary {
  color: #1976d2;
}

/* Allow horizontal scrolling on narrower screens */
.scrollable-table-container {
  overflow-x: auto;
}

/* Striping for the outer table rows */
.striped-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

/* Hover effect on outer table rows */
.hoverable-row:hover {
  background-color: #e3f2fd;
}

/* Confusion matrix container: ensure it doesn’t overflow */
.nested-matrix-container {
  overflow-x: auto;
  margin: 0 auto;
}

/* Collapse nested table borders slightly */
.nested-matrix-table th,
.nested-matrix-table td {
  padding: 4px 6px;
  border-width: 1px !important;
  font-size: 0.75rem;
}

/* Center the nested table horizontally */
.nested-matrix-container .nested-matrix-table {
  margin: 0 auto;
}

/* Highlight true-positive diagonal cells in the confusion matrix */
.bg-green-2 {
  background-color: #e8f5e9 !important;
}

/* Ensure the main card has a subtle border and background */
q-card {
  background-color: #ffffff;
  border-radius: 8px;
}

/* Reduce padding on table cells for a tighter look */
q-markup-table td,
q-markup-table th {
  padding: 8px 12px;
}

/* Header row text styling */
q-markup-table thead th {
  font-weight: 600;
}
</style>
