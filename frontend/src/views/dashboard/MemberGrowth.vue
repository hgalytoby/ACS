<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useChartStore } from '@/stores/chart'
import { getLineChartRandomColor } from '@/utils/misc'
import { useTheme } from 'vuetify'

const vuetifyTheme = useTheme()
const chartStore = useChartStore()
const series = ref([])
const subtitle = ref()
const colors = getLineChartRandomColor()

const switchVuetifyTheme = () => {
  return {
    ...chartOptions.value,
    tooltip: {
      theme: vuetifyTheme.global.name.value,
    },
  }
}

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
  tooltip: {
    theme: vuetifyTheme.global.name.value,
  },
})

watch(vuetifyTheme.name, (nv, ov) => {
  chartOptions.value = switchVuetifyTheme()
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
      ...switchVuetifyTheme(),
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

