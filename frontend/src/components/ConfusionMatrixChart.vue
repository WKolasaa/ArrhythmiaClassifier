<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const chartData = {
  labels: ['Normal', 'AFib', 'PVC'],
  datasets: [
    {
      label: 'Predicted Normal',
      data: [95, 41, 2],
      backgroundColor: '#42A5F5'
    },
    {
      label: 'Predicted AFib',
      data: [2, 8, 47],
      backgroundColor: '#66BB6A'
    },
    {
      label: 'Predicted PVC',
      data: [1, 1, 5],
      backgroundColor: '#FFA726'
    }
  ]
}

const chartOptions = {
  responsive: true,
  indexAxis: 'y',
  scales: {
    x: { stacked: true },
    y: { stacked: true }
  },
  plugins: {
    legend: { position: 'bottom' },
    title: { display: true, text: 'Confusion Matrix (True vs Predicted)' }
  }
}
</script>
