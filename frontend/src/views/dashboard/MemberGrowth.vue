<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useChartStore } from '@/stores/chart'
import { getLineChartRandomColor } from '@/utils/misc'

const chartStore = useChartStore()
const series = ref([])
const subtitle = ref()

const color = [
  {
    borderColor: 'rgba(54, 162, 235, 1)',
    backgroundColor: 'rgba(54, 162, 235, 0.2)',
  },
  {
    borderColor: 'rgba(255, 99, 132,1)',
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
  },
  {
    borderColor: 'rgba(75, 192, 192, 1)',
    backgroundColor: 'rgba(75, 192, 192, 0.2)',
  },
  {
    borderColor: 'rgba(255, 206, 86, 1)',
    backgroundColor: 'rgba(255, 206, 86, 0.2)',
  },
  {
    borderColor: 'rgba(255, 159, 64, 1)',
    backgroundColor: 'rgba(255, 159, 64, 0.2)',
  },
  {
    borderColor: 'rgba(153, 102, 255, 1)',
    backgroundColor: 'rgba(153, 102, 255, 0.2)',
  },
]

const colors = getLineChartRandomColor()

const chartOptions = ref({
  chart: {
    type: 'line',
    zoom: {
      enabled: false,
    },
    toolbar: {
      show: false,
    },
  },
  stroke: {
    curve: 'smooth',
    lineCap: 'butt',
    width: 2,
    colors: [colors.borderColor],
    shape: 'circle',
  },
  markers: {
    size: 4,
    colors: colors.borderColor,
    hover: {
      size: 6,
    },
  },
})

watch(
  () => chartStore.memberGrowthData,
  (nv, ov) => {
    const labels = []
    const data = []

    chartStore.memberGrowthData.forEach(item => {
      labels.push(item.date)
      data.push(item.count)
    })
    series.value = [{ name: '成員成長圖', data }]
    subtitle.value = `${labels.at(0)} ~ ${labels.at(-1)}`
    chartOptions.value = {
      labels,
    }
  },
  { deep: true },
)
</script>

<template>
  <VCard>
    <VCardTitle class="align-start">
      <span class="font-weight-semibold">成員成長圖</span>
    </VCardTitle>
    <VCardSubtitle class="text-center text-sm-h6">
      {{ subtitle }}
    </VCardSubtitle>
    <VCardText>
      <VSelect class="text-end" />
    </VCardText>
    <VCardText>
      <VueApexCharts
        height="400px"
        :options="chartOptions"
        :series="series"
      />
    </VCardText>
  </VCard>
</template>

