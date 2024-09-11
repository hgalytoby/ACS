<script setup>
import { useMemberStore } from '@/stores/member'
import MyVImg from '@/components/MyVImg.vue'

const memberStore = useMemberStore()

memberStore.memberStatusList()
</script>

<template>
  <VRow>
    <VCol
      v-for="status in memberStore.statusList"
      :key="status.memberLocation.id"
      cols="12"
      sm="6"
    >
      <VCard class="mx-auto">
        <MyVImg
          :img-obj="{
            cover: true,
            src: status.memberLocation.image,
            lazySrc: status.memberLocation.image,
          }"
        />
        <VCardTitle>{{ status.memberLocation.name }}</VCardTitle>
        <VDivider />
        <div class="d-flex py-3 justify-space-between">
          <VListItem
            v-for="member in status.memberList"
            :key="member.id"
            class="w-100"
          >
            <template #prepend>
              <VAvatar
                :image="member.image"
                size="x-large"
              />
            </template>
            <div>
              <VBtn class="d-none d-md-block float-md-end">
                test
              </VBtn>
            </div>


            <div class="d-flex my-n2 justify-sm-start justify-md-space-between">
              <VListItem prepend-icon="mdi-account-outline">
                <VListItemSubtitle>{{ member.name }}</VListItemSubtitle>
              </VListItem>
              <VListItem prepend-icon="mdi-domain">
                <VListItemSubtitle>{{ member.company }}</VListItemSubtitle>
              </VListItem>
              <VListItem prepend-icon="mdi-card-account-details-outline">
                <VListItemSubtitle>{{ member.jobTitle }}</VListItemSubtitle>
              </VListItem>
            </div>
            <div class="my-n2">
              <VListItem prepend-icon="mdi-calendar-outline">
                <VListItemSubtitle>{{ member.createdAt }}</VListItemSubtitle>
              </VListItem>
            </div>
          </VListItem>
        </div>
      </VCard>
    </VCol>
  </VRow>
</template>

