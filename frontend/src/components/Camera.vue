<script setup>
import { QrcodeStream } from 'vue-qrcode-reader'
import { useAcceptStore } from '@/stores/accept'
import Swal from 'sweetalert2'
import CameraDialogs from '@/components/CameraDialogs.vue'

const props = defineProps({
  showTitle: {
    type: Boolean,
    required: true,
  },
  width: {
    type: Number,
    required: false,
  },
})

const acceptStore = useAcceptStore()
const dialog = ref(null)
const locationId = ref(undefined)
const status = ref(true)
const paused = ref(false)
const error = ref()

acceptStore.acceptLocation()
acceptStore.acceptApi()

const paintOutline = (detectedCodes, ctx) => {
  for (const detectedCode of detectedCodes) {
    const [firstPoint, ...otherPoints] = detectedCode.cornerPoints

    ctx.strokeStyle = 'red'

    ctx.beginPath()
    ctx.moveTo(firstPoint.x, firstPoint.y)
    for (const { x, y } of otherPoints) {
      ctx.lineTo(x, y)
    }
    ctx.lineTo(firstPoint.x, firstPoint.y)
    ctx.closePath()
    ctx.stroke()
  }
}

const acceptMemberStatus = async payload => {
  await acceptStore.acceptMemberStatus(payload)
    .then(async () => {
      await dialog.value.openDialog()
    }).catch(async err => {
      await Swal.fire({
        title: '失敗123',
        text: err.response.data.detail,
        icon: 'error',
      }).then(() => {
        paused.value = false
      })
    })
}

const dialogClose = () => {
  paused.value = false
}

const errorCallback = msg => {
  console.log('camera')
  console.dir(msg)

  if (msg.message === 'Requested device not found'){
    error.value = '沒有找到攝影機'
  } else {
    error.value = ''
  }
}

const onDetect = async ([ detectedCode ]) => {
  const {
    id: memberId,
    project,
  } = JSON.parse(window.atob(detectedCode.rawValue))

  paused.value = true

  if (!locationId.value){
    Swal.fire(
      {
        title: '尚未選擇地區',
        text: '請選擇地區!',
        icon: 'error',
        allowOutsideClick: false,
      }).then(() => {
      paused.value = false
    })
  } else {
    await acceptMemberStatus({
      status: status.value,
      memberId,
      memberLocationId: locationId.value,
      project,
    })
  }
}

const timeout = ms => {
  return new Promise(resolve =>{
    window.setTimeout(resolve, ms)
  })
}
</script>


<template>
  <div>
    <VCard
      class="auth-card pa-4 pt-7"
      :max-width="props.width"
    >
      <VCardItem
        v-if="props.showTitle"
        class="justify-center"
      >
        <template #prepend>
          <VIcon
            icon="mdi-door-sliding-lock"
            color="primary"
            size="30px"
          />
        </template>

        <VCardTitle
          class="font-weight-semibold text-2xl text-uppercase"
          title="Access Control System"
        >
          ACS
        </VCardTitle>
      </VCardItem>
      <p class="mb-2 text-center camera-error">
        {{ error }}
      </p>
      <p class="text-2xl font-weight-semibold text--primary text-center">
        <VIcon
          size="x-large"
          icon="mdi-qrcode-scan"
        />
        請掃描 Qrcode
      </p>
      <VCardText class="pt-2">
        <VSelect
          v-model="locationId"
          hide-details
          :items="acceptStore.acceptLocationList"
          label="請選擇地區"
          item-title="name"
          item-value="id"
        />
      </VCardText>
      <VCardItem class="justify-center ma-n5">
        <VRadioGroup
          v-model="status"
          inline
        >
          <VRadio
            label="進入"
            :value="true"
          />
          <VRadio
            label="離開"
            :value="false"
          />
        </VRadioGroup>
      </VCardItem>
      <VCardText>
        <qrcode-stream
          :paused="paused"
          :track="paintOutline"
          @detect="onDetect"
          @error="errorCallback"
        />
      </VCardText>
    </VCard>
    <CameraDialogs
      ref="dialog"
      @close-event="dialogClose"
    />
  </div>
</template>

<style lang="scss" scoped>
.camera-error {
  color: red;
}
</style>
