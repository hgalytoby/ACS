import { defineStore } from 'pinia'
import {
  reqMemberList,
  reqMemberCreateOrUpdate,
  reqMember,
  reqMemberDestroy,
  reqMemberRecordList,
  reqMemberRecordCreate,
  reqMembersLocationList,
  reqMembersLocationCreateOrUpdate,
  reqMembersLocationDestroy,
} from '@/api/member'
import { useToast } from 'vue-toastification'

const toast = useToast()

export const useMemberStore = defineStore({
  id: 'useMemberStore',
  state: () => ({
    list: {
      items: [],
      pages: 1,
      total: 1,
    },
    recordList: {
      items: [],
      pages: 1,
      total: 1,
    },
    statusList: [],
    statusInfoList: [],
    locationList: [],
  }),
  actions: {
    async memberList(params) {
      await reqMemberList(params).then(({ data }) => {
        this.$patch({ list: data })
      })
    },
    async memberCreateOrUpdate(payload) {
      await reqMemberCreateOrUpdate(payload)
        .then(() => {
          if (payload?.id){
            toast.success('更新成功!')
          } else {
            toast.success('新增成功!')
            this.$router.push({ name: 'MemberList' })
          }
        })
        .catch(() => {
        })
    },
    async member(memberId) {
      return await reqMember(memberId)
        .then(({ data }) => data)
    },
    async memberDestroy(memberId) {
      await reqMemberDestroy(memberId)
        .then(() => {})
        .catch(() => {})
    },
    async memberRecordList(params) {
      await reqMemberRecordList(params)
        .then(({ data }) => {
          this.$patch({ recordList: data })
        }).catch(err => {})
    },
    async memberRecordCreate(payload) {
      await reqMemberRecordCreate(payload)
        .then(() => {})
        .catch(err => {})
    },
    async memberLocationList() {
      await reqMembersLocationList()
        .then(({ data }) => {
          this.$patch({ locationList: data })
        })
        .catch(err => {})
    },
    async memberLocationCreateOrUpdate(payload) {
      await reqMembersLocationCreateOrUpdate(payload)
        .then(() => {})
        .catch(err => {})
    },
    async memberLocationDestroy(locationId) {
      await reqMembersLocationDestroy(locationId)
        .then(() => {})
        .catch(err => {})
    },
  },
})
