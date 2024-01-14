<script setup>
import { useChartStore } from '@/stores/chart'
import VueApexCharts from 'vue3-apexcharts'
import { useTheme } from 'vuetify'

const vuetifyTheme = useTheme()
const chartStore = useChartStore()
const series = ref([])


const getColors = alpha => [
  `rgba(54, 162, 235, ${alpha})`,
  `rgba(255, 99, 132,${alpha})`,
  `rgba(75, 192, 192, ${alpha})`,
  `rgba(255, 206, 86, ${alpha})`,
  `rgba(255, 159, 64, ${alpha})`,
  `rgba(153, 102, 255, ${alpha})`,
  `rgba(255, 0, 255, ${alpha})`,
]

const getLegendPosition = value => window.innerWidth >= 1281 ? 'right' : 'top'

const chartOptions = ref({
  chart: {
    type: 'donut',
  },
  legend: {
    position: getLegendPosition(window.innerWidth),
  },
  stroke: {
    colors: getColors(1),
  },
})

const switchVuetifyTheme = () => {
  let colors, fillColors, dataLabelsColor
  const legendColors = getColors(1)
  if (vuetifyTheme.name.value === 'light') {
    colors = getColors(0.2)
    fillColors = getColors(0.5)
    dataLabelsColor = 'rgba(0,0,0, 0.5)'
  } else {
    colors = getColors(0.6)
    fillColors = getColors(0.5)
    dataLabelsColor = 'rgba(255,255,255, 0.8)'
  }

  return {
    colors,
    legend: {
      labels: {
        colors: legendColors,
      },
      markers: {
        fillColors,
      },
    },
    dataLabels: {
      style: {
        colors: [
          dataLabelsColor,
        ],
      },
    },
  }
}

watch(vuetifyTheme.name, (nv, ov) => {
  chartOptions.value = switchVuetifyTheme()
})

watch(
  () => chartStore.emailLogClassificationData,
  (nv, ov) => {
    const data = chartStore.emailLogClassificationData.labels.reduce((obj, label) => {
      obj[label] = 0

      return obj
    }, {})

    chartStore.emailLogClassificationData.items.forEach(item => {
      data[item.label] = item.data
    })
    series.value = Object.values(data)
    chartOptions.value = {
      ...switchVuetifyTheme(),
      labels: chartStore.emailLogClassificationData.labels,
    }
  },
  { deep: true },
)

onMounted(() => {
  window.onresize = () => {
    chartOptions.value = {
      legend: {
        position: getLegendPosition(window.innerWidth),
      },
    }
  }
})
</script>

<template>
  <VCard>
    <VCardTitle class="align-start">
      <span class="font-weight-semibold">硬碟容量詳細圖</span>
    </VCardTitle>
    <VCardText>
      <VueApexCharts
        height="400px"
        :options="chartOptions"
        :series="series"
      />
    </VCardText>
  </VCard>
</template>
