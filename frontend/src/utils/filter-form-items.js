import { getCreatedAt } from '@/utils/misc'

export const getAccountSettingsUserListFilterFormItems = () => {
  const route = useRoute()

  return {
    event: route.query.event,
    createdAt: getCreatedAt(route.query.createdAt),
  }
}
export const getSettingsUserListFilterFormItems = () => {
  const route = useRoute()

  return {
    email: route.query.email,
    username: route.query.username,
    createdAt: getCreatedAt(route.query.createdAt),
  }
}

export const getSettingsUserLogFilterFormItems = () => {
  const route = useRoute()

  return {
    event: route.query.event,
    email: route.query.email,
    username: route.query.username,
    createdAt: getCreatedAt(route.query.createdAt),
  }
}

export const getMemberListFilterFormItems = () => {
  const route = useRoute()

  return {
    name: route.query.name,
    bloodType: route.query.bloodType,
    phone: route.query.phone,
    company: route.query.company,
    jobTitle: route.query.jobTitle,
    createdAt: getCreatedAt(route.query.createdAt),
  }
}
export const getSystemLogFilterFormItems = () => {
  const route = useRoute()

  return {
    event: route.query.event,
    createdAt: getCreatedAt(route.query.createdAt),
  }
}

export const getMemberRecordListFilterFormItems = () => {
  const route = useRoute()

  return {
    status: route.query.status,
    memberLocationName: route.query.memberLocationName,
    memberName: route.query.memberName,
    memberPhone: route.query.memberPhone,
    memberCompany: route.query.memberCompany,
    memberJobTitle: route.query.memberJobTitle,
    createdAt: getCreatedAt(route.query.createdAt),
  }
}

