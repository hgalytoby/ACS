<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useChartStore } from '@/stores/chart'
import { useTheme } from 'vuetify'

const vuetifyTheme = useTheme()
const chartStore = useChartStore()

const series = ref([])

const subtitle = ref()


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
    type: 'bar',
    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    bar: {
      distributed: true, // 將顏色分佈到每個長條\
    },
  },
  legend: {
    show: false,
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

    chartStore.memberRecordHourlyCountData.data.forEach(item => {
      labels.push(item.hour)
      data.push(item.count)
    })
    series.value = [{ name: '進出時段紀錄圖', data }]
    subtitle.value = `${labels.at(0)} ~ ${labels.at(-1)}`
    chartOptions.value = {
      ...switchVuetifyTheme(),
      xaxis: {
        categories: labels,
      },
      yaxis: {
        axisBorder: {
          show: true,
        },
        range: 10000,
      },
    }
  },
  { deep: true },
)
</script>

<template>
  <VCard>
    <VCardTitle class="align-start">
      <span class="font-weight-semibold">進出時段紀錄圖</span>
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

