<script setup>
import MyVImg from '@/components/MyVImg.vue'
import { useAcceptStore } from '@/stores/accept'
import SweetalertIcon from 'vue-sweetalert-icons'

const emit = defineEmits(['closeEvent'])
const dialog = ref(false)
const acceptStore = useAcceptStore()

const openDialog = async payload => {
  dialog.value = true
}

const updateDialogEvent = () => {
  dialog.value = false
  emit('closeEvent')
}

defineExpose({
  openDialog,
})
</script>

<template>
  <div class="text-center">
    <VDialog
      v-model="dialog"
      width="auto"
      @update:model-value="updateDialogEvent"
    >
      <VCard width="448">
        <VCardTitle>
          <MyVImg
            :img-obj="{
              class:'mt-3',
              src: acceptStore.member.memberLocation.image,
              lazySrc: acceptStore.member.memberLocation.image,
            }"
          />
        </VCardTitle>
        <SweetalertIcon icon="success" />
        <VCardTitle class="d-flex flex-column justify-center align-center">
          <h6 class="text-h6">
            {{ acceptStore.member.status ? '進入' : '離開' }}{{ acceptStore.member.memberLocation.name }}地點
          </h6>
        </VCardTitle>
        <VCardTitle />
        <div class="ma-auto">
          <MyVImg
            :img-obj="{
              class: 'rounded',
              width: '200',
              src: acceptStore.member.member.image,
              lazySrc: acceptStore.member.member.image,
            }"
          />
        </div>
        <VCardText class="d-flex justify-center">
          <div class="me-auto pe-4">
            <p class="d-flex align-center mb-6">
              <VIcon
                color="primary"
                icon="mdi-account-outline"
              />
              <span class="ms-3">{{ acceptStore.member.member.name }}</span>
            </p>

            <p class="d-flex align-center mb-0">
              <VIcon
                color="primary"
                icon="mdi-card-account-details-outline"
              />
              <span class="ms-3">{{ acceptStore.member.member.jobTitle }}</span>
            </p>
          </div>
          <div class="ms-auto ps-4">
            <p class="d-flex align-center mb-6">
              <VIcon
                color="primary"
                icon="mdi-domain"
              />
              <span class="ms-3">{{ acceptStore.member.member.company }}</span>
            </p>

            <p class="d-flex align-center mb-0">
              <VIcon
                color="primary"
                icon="mdi-phone-outline"
              />
              <span class="ms-3">{{ acceptStore.member.member.phone }}e</span>
            </p>
          </div>
        </VCardText>
        <VDivider />
        <VCardActions class="justify-center">
          <VBtn @click="updateDialogEvent">
            確定
          </VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </div>
</template>
