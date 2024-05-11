<script setup>
import { ErrorMessage, Field } from 'vee-validate'
import { useEmailStore } from '@/stores/email'

const props = defineProps({
  event: {
    type: String,
  },
})

const emailStore = useEmailStore()
const subject = defineModel({ type: String })
</script>

<template>
  <VCardTitle>
    目前主旨: {{ emailStore[event].subject }}
  </VCardTitle>
  <VCardTitle>
    預覽內容:
  </VCardTitle>
  <VCardItem class="mt-n5">
    <VTextarea
      readonly
      :model-value="subject"
      class="my-1"
      density="compact"
      variant="solo-filled"
      type="input"
      auto-grow
      rows="1"
    />
  </VCardItem>
  <VCardItem class="mt-n5">
    <Field
      v-slot="{ field }"
      v-model="subject"
      name="subject"
      type="text"
    >
      <VTextField
        v-bind="field"
        v-model="subject"
        class="my-1"
        density="compact"
        label="Subject"
        type="input"
      />
    </Field>
    <ErrorMessage
      class="error-message"
      name="subject"
    />
  </VCardItem>
</template>
