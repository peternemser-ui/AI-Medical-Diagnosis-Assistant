<template>
  <div v-if="chartData">
    <Pie :data="chartData" :options="options" />
  </div>
</template>

<script setup>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const props = defineProps({
  rawText: String
})

const parseData = (text) => {
  const lines = text.split('\n').filter(line => line.includes('Confidence'))
  const labels = []
  const values = []

  lines.forEach(line => {
    const match = line.match(/(.*?) - Confidence: (\d+)%/)
    if (match) {
      labels.push(match[1].trim())
      values.push(parseInt(match[2]))
    }
  })

  return { labels, values }
}

const { labels, values } = parseData(props.rawText)

const chartData = {
  labels,
  datasets: [{
    label: 'Diagnosis Confidence',
    data: values,
    backgroundColor: ['#4CAF50', '#2196F3', '#FF9800']
  }]
}

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
}
</script>
