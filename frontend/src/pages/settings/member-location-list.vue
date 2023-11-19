<script setup>
import { useMemberStore } from '@/stores/member'
import MyVImg from '@/components/MyVImg.vue'
import Swal from 'sweetalert2'
import SettingsMemberLocationCreate from '@/views/pages/settings/SettingsMemberLocationCreate.vue'

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
    if (result.isConfirmed) {
      await Swal.fire({
        title: '已刪除!',
        icon: 'success',
      })
    }
  })
}

const update = location => {
  dialog.value.resetImgModel()
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
        <VCard class="d-flex align-center justify-center location-image my-3">
          <VBtn
            icon="mdi-plus"
            @click="openDialog"
          />
        </VCard>
      </VCol>
      <transition-group
        appear
        name="animate__animated animate__bounce"
        enter-active-class="animate__fadeIn"
        leave-active-class="animate__fadeOut"
      >
        <VCol
          v-for="location in memberStore.locationList"
          :key="location.id"
          cols="12"
          sm="6"
          md="4"
        >
          <VCard class="location-image my-card overflow-visible my-3">
            <MyVImg
              :img-obj="{
                src: location.image,
                lazySrc: location.image,
                cover: true,
                aspectRatio: 2.4,
                class: 'cardImage rounded',
                style: 'z-index: 10'
              }"
            />
            <VCardActions class="justify-center mt-n8">
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
            <VCardTitle class="text-center">
              <span>地點名稱: {{ location.name }}</span>
            </VCardTitle>
          </VCard>
        </VCol>
      </transition-group>
    </VRow>
    <SettingsMemberLocationCreate ref="dialog" />
  </div>
</template>

<style scoped lang='scss'>
.my-card {

  .cardImage {
    transition: transform 0.2s ease-in;
  }

  &:hover .cardImage {
    transform: translate(0, -30px);
  }
}
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
