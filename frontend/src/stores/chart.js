import { defineStore } from 'pinia'
import {
  reqMemberGrowth,
  reqNewMemberGrowth,
  reqMemberRecordGrowth,
  reqMemberRecordHourlyCount,
  reqAllChart,
} from '@/api/chart'

export const useChartStore = defineStore({
  id: 'useChartStore',
  state: () => ({
    hardDiskVolume: {},
    emailLogClassification: [],
    memberGrowth: {},
    newMemberGrowth: {},
    memberRecordGrowth: {},
    memberRecordHourlyCount: {},
  }),
  actions: {
    async memberGrowth() {
      await reqMemberGrowth().then(({ data }) => {
        this.$patch({ memberGrowth: data })
      })
    },
    async newMemberGrowth() {
      await reqNewMemberGrowth().then(({ data }) => {
        this.$patch({ newMemberGrowth: data })
      })
    },
    async memberRecordGrowth() {
      await reqMemberRecordGrowth().then(({ data }) => {
        this.$patch({ memberRecordGrowth: data })
      })
    },
    async memberRecordHourlyCount() {
      await reqMemberRecordHourlyCount().then(({ data }) => {
        this.$patch({ memberRecordHourlyCount: data })
      })
    },
    async allAllChart() {
      await reqAllChart().then(({ data }) => {
        this.$patch(data)})
    },
  },
})
