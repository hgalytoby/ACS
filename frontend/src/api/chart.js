import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqHardDiskVolume = params => jwtRequest.get(urls.chart.hardDiskVolume)

export const reqEmailLogClassification = params => jwtRequest.get(urls.chart.emailLogClassification)

export const reqMemberGrowth = params => jwtRequest.get(urls.chart.memberGrowth)

export const reqNewMemberGrowth = params => jwtRequest.get(urls.chart.newMemberGrowth)

export const reqMemberRecordGrowth = params => jwtRequest.get(urls.chart.memberRecordGrowth)

export const reqMemberRecordHourlyCount = params => jwtRequest.get(urls.chart.memberRecordHourlyCount)

export const reqAllChart = params => jwtRequest.get(urls.chart.allChart)
