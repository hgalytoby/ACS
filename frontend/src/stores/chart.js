import { defineStore } from 'pinia'
import {
  reqMemberGrowth,
  reqNewMemberChart,
  reqMemberRecordGrowth,
  reqMemberRecordHourlyCount,
  reqAllChart,
} from '@/api/chart'

export const useChartStore = defineStore({
  id: 'useChartStore',
  state: () => ({
    hardDiskVolumeData: { items: [], labels: [] },
    emailLogClassificationData: { items: [], labels: [] },
    memberGrowthData: [],
    newMemberChartData: [],
    memberRecordGrowthData: [],
    memberRecordHourlyCountData: [],
  }),
  actions: {
    async memberGrowth() {
      await reqMemberGrowth().then(({ data }) => {
        this.$patch({ memberGrowthData: data })
      })
    },
    async newMemberGrowth() {
      await reqNewMemberChart().then(({ data }) => {
        this.$patch({ newMemberChartData: data })
      })
    },
    async memberRecordGrowth() {
      await reqMemberRecordGrowth().then(({ data }) => {
        this.$patch({ memberRecordGrowthData: data })
      })
    },
    async memberRecordHourlyCount() {
      await reqMemberRecordHourlyCount().then(({ data }) => {
        this.$patch({ memberRecordHourlyCountData: data })
      })
    },
    async allAllChart() {
      await reqAllChart().then(({ data }) => {
        this.$patch({
          hardDiskVolumeData: data.hardDiskVolume,
          emailLogClassificationData: data.emailLogClassification,
          memberGrowthData: data.memberGrowth,
          newMemberChartData: data.newMemberChart,
          memberRecordGrowthData: data.memberRecordGrowth,
          memberRecordHourlyCountData: data.memberRecordHourlyCount,
        })
      })
    },
  },
})
