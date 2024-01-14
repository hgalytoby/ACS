<script setup>
import { useChartStore } from '@/stores/chart'
import HardDiskVolume from '@/views/dashboard/HardDiskVolume.vue'
import EmailLogClassification from '@/views/dashboard/EmailLogClassification.vue'
import MemberGrowth from '@/views/dashboard/MemberGrowth.vue'
import NewMemberGrowth from '@/views/dashboard/NewMemberGrowth.vue'
import MemberRecordGrowth from '@/views/dashboard/MemberRecordGrowth.vue'
import MemberRecordHourlyCount from '@/views/dashboard/MemberRecordHourlyCount.vue'

const chartStore = useChartStore()

chartStore.allAllChart()
</script>

<template>
  <VRow>
    <VCol
      cols="12"
      sm="6"
    >
      <HardDiskVolume />
    </VCol>
    <VCol
      cols="12"
      sm="6"
    >
      <EmailLogClassification />
    </VCol>
    <VCol
      cols="12"
      sm="6"
    >
      <MemberGrowth />
    </VCol>
    <VCol
      cols="12"
      sm="6"
    >
      <NewMemberGrowth />
    </VCol>
    <VCol cols="12">
      <MemberRecordGrowth />
    </VCol>
    <VCol cols="12">
      <MemberRecordHourlyCount />
    </VCol>
  </VRow>
</template>
