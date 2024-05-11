<script setup>
import { ErrorMessage, Field } from 'vee-validate'
import { useEmailStore } from '@/stores/email'

const props = defineProps({
  event: {
    type: String,
  },
  bodyRule: {
    type: Object,
    default: null,
    required: false,
  },
})

const emailStore = useEmailStore()
const body = defineModel({ type: String })
const bodyShow = computed(() => props.bodyRule ? props.bodyRule.show(body.value) : body.value)
</script>

<template>
  <VCardTitle>
    目前內容:
  </VCardTitle>
  <VCardItem class="mt-n5">
    <VTextarea
      readonly
      :model-value="emailStore[event].body"
      class="my-1"
      density="compact"
      variant="solo-filled"
      type="input"
      auto-grow
    />
  </VCardItem>
  <VCardTitle>
    預覽內容:
  </VCardTitle>
  <VCardItem class="mt-n5">
    <VTextarea
      :model-value="bodyShow"
      readonly
      class="my-1"
      density="compact"
      variant="solo-filled"
      type="input"
      auto-grow
    />
  </VCardItem>
  <VCardTitle>
    修改內容:
  </VCardTitle>
  <VCardItem class="mt-n5">
    <Field
      v-slot="{ field }"
      v-model="body"
      name="body"
      type="text"
    >
      <VTextarea
        v-bind="field"
        v-model="body"
        class="my-1"
        clearable
        density="compact"
        type="input"
        auto-grow
      />
    </Field>
    <ErrorMessage
      class="error-message"
      name="body"
    />
  </VCardItem>
</template>

