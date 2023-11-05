<script setup>
import { useMemberStore } from '@/stores/member'
import MyVImg from '@/components/MyVImg.vue'
import Swal from 'sweetalert2'
import SettingsMemberLocationCarete from '@/views/pages/settings/SettingsMemberLocationCarete.vue'

const memberStore = useMemberStore()
const dialog = ref(null)

memberStore.memberLocationList()

const destroy = async locationId => {
  await Swal.fire({
    title: '要刪除地點嗎?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: '確定',
    cancelButtonText: '取消',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      await memberStore.memberLocationDestroy(locationId)
        .then(async () => {
          await memberStore.memberLocationList()
        })
        .catch(async err => {
          await Swal.showValidationMessage(err.response.data.detail)
        })
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then(async result => {
    console.log(result.value)
    if (result.isConfirmed) {
      await Swal.fire({
        title: '已刪除!',
        icon: 'success',
      })
    }
  })
}

const update = location => {
  dialog.value.openDialog(location)
}

const openDialog = () => {
  dialog.value.openDialog()
}
</script>

<template>
  <div>
    <VRow>
      <VCol
        cols="12"
        sm="6"
        md="4"
      >
        <VCard class="d-flex align-center justify-center location-image">
          <VBtn
            icon="mdi-plus"
            @click="openDialog"
          />
        </VCard>
      </VCol>
      <VCol
        v-for="location in memberStore.locationList"
        :key="location.id"
        cols="12"
        sm="6"
        md="4"
      >
        <VCard class="location-image">
          <MyVImg
            class="position-relative"
            style="z-index: 3"
            :img-obj="{
              src: location.image,
              lazySrc: location.image,
              maxHeight: 256,
            }"
          />
          <VCardTitle class="text-center">
            <span>地點名稱: {{ location.name }}</span>
          </VCardTitle>
          <VCardActions class="justify-center">
            <VBtn
              color="success"
              icon="mdi-pencil"
              @click="update(location)"
            />
            <VBtn
              color="error"
              icon="mdi-trash-can-outline"
              @click="destroy(location.id)"
            />
          </VCardActions>
        </VCard>
      </VCol>
    </VRow>
    <SettingsMemberLocationCarete ref="dialog" />
  </div>
</template>

<style scoped lang='scss'>
@media (max-width: 959px) {
  .location-image {
    height: 228px;
  }
}

@media (min-width: 960px) and (max-width: 1279px) {
  .location-image {
    height: 224px;
  }
}

@media (min-width: 1280px) {
  .location-image {
    height: 288px;
  }
}
</style>
