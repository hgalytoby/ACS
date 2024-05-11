import { jwtRequest } from '@/utils/requests'
import urls from '@/api/urls'

export const reqMemberList = params => jwtRequest.get(urls.member.members, { params })

export const reqMemberCreateOrUpdate = payload => {
  if (payload.get('id')) {
    return jwtRequest.patch(urls.member.member(payload.get('id')), payload)
  }

  return jwtRequest.post(urls.member.members, payload)
}

export const reqMember = memberId => jwtRequest.get(urls.member.member(memberId))

export const reqMemberDestroy = memberId => jwtRequest.delete(urls.member.member(memberId))

export const reqMemberRecordList = params => jwtRequest.get(urls.member.membersRecord, { params })

export const reqMemberRecordCreate = payload => jwtRequest.post(urls.member.membersRecord, payload)

export const reqMembersLocationList = () => jwtRequest.get(urls.member.membersLocation)

export const reqMembersLocationCreateOrUpdate = payload => {
  if (payload.get('id')) {
    return jwtRequest.patch(urls.member.memberLocation(payload.get('id')), payload)
  }

  return jwtRequest.post(urls.member.membersLocation, payload)
}

export const reqMembersLocationDestroy = locationId => jwtRequest.delete(urls.member.memberLocation(locationId))

