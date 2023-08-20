<script setup>
import { QrcodeStream } from 'vue-qrcode-reader'
import { useAcceptStore } from '@/stores/accept'

const acceptStore = useAcceptStore()

const locationId = ref(undefined)
const error = ref()
const status = ref(true)

const paused = ref(false)
const result = ref(null)
const base64 = ref('')
const isValid = ref(undefined)

acceptStore.acceptLocation()
acceptStore.acceptApi()

const selectChange = e => {
  console.log('e', e)
}

const resetValidationState = () => {
  isValid.value = undefined
}

const validationPending = computed(
  () => isValid.value === undefined && paused.value,
)

const onDetect = async ([ firstDetectedCode ]) => {
  result.value = firstDetectedCode.rawValue
  paused.value = true

  // pretend it's taking really long
  await timeout(3000)
  isValid.value = result.value.startsWith('http')

  // some more delay, so users have time to read the message
  await timeout(2000)
  paused.value = false
}

const timeout = ms => {
  return new Promise(resolve =>{
    window.setTimeout(resolve, ms)
  })
}

const validationSuccess = computed(
  () => isValid.value === true,
)

const validationFailure = computed(
  () => isValid.value === false,
)
</script>


<template>
  <VCard
    class="auth-card pa-4 pt-7"
    max-width="448"
  >
    <VCardItem class="justify-center">
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

    <VCardText class="pt-2">
      <VSelect
        v-model="locationId"
        hide-details
        :items="[{id: '1', name: 'A'}, {id: '2', name: 'B'}]"
        label="請選擇地區"
        item-title="name"
        item-value="id"
        @change="selectChange"
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
      <div>
        <p class="decode-result">
          Last result: <b>{{ result }}</b>
        </p>

        <qrcode-stream
          :paused="paused"
          @detect="onDetect"
          @error="console.error"
          @camera-on="resetValidationState"
        />
      </div>
    </VCardText>
  </VCard>
</template>

<style lang='scss'>
.camera-error {
  font-weight: bold;
  color: red;
}
.validation-success,
.validation-failure,
.validation-pending {
  position: absolute;
  width: 100%;
  height: 100%;

  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  text-align: center;
  font-weight: bold;
  font-size: 1.4rem;
  color: black;

  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
}
.validation-success {
  color: green;
}
.validation-failure {
  color: red;
}
.qrcode-stream-camera{
  width: 100%;
}
.qrcode-stream-overlay{
  position: absolute;
  top: 10px;
  left: 0;
}
</style>
