<script setup>
import { Form } from 'vee-validate'
import * as yup from 'yup'
import { useEmailStore } from '@/stores/email'
import EmailSubject from '@/views/pages/settings/email-settings/EmailSubject.vue'
import EmailBody from '@/views/pages/settings/email-settings/EmailBody.vue'

const props = defineProps({
  event: {
    type: [String],
    required: true,
  },
  bodyRule: {
    type: Object,
    default: null,
    required: false,
  },
})

const defaultBodySchema = yup.string().required()

const formSchema = yup.object({
  subject: yup.string().required(),
  body: props.bodyRule ? props.bodyRule.schema : defaultBodySchema,
})

const emailStore = useEmailStore()

const subject = ref()
const body = ref()

watch(emailStore[props.event], (nV, oV) => {
  body.value = nV.body
  subject.value = nV.subject
}, {
  immediate: true,
})

async function submit({ subject, body }, $event) {
  const event = $event.evt.submitter.dataset.event
  if (event === 'try') {
    await emailStore.settingTrySend({ subject, body, event: props.event })
  } else {
    await emailStore.settingUpdate({ subject, body, event: props.event })
    await emailStore.setting(props.event)
  }
}
</script>

<template>
  <VRow>
    <VCol cols="12">
      <Form
        :validation-schema="formSchema"
        @submit="submit"
      >
        <VCard class="pa-3 mt-2">
          <EmailSubject
            v-model="subject"
            :event="event"
          />
          <VDivider />
          <EmailBody
            v-model="body"
            :event="event"
            :body-rule="bodyRule"
          />
          <VBtn
            class="my-2"
            block
            color="teal"
            type="submit"
            data-event="try"
          >
            <VIcon icon="mdi-email-fast-outline" />
            測試
          </VBtn>
          <VBtn
            class="my-2"
            block
            color="primary"
            type="submit"
            data-event="update"
          >
            <VIcon icon="mdi-email-check-outline" />
            儲存
          </VBtn>
        </VCard>
      </Form>
    </VCol>
  </VRow>
</template>

