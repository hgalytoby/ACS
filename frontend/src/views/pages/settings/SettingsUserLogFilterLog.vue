<script setup>
import { userLogSelectItem } from '@/utils/filter-select-item'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import DatePicker from 'vue-datepicker-next'
import useFilter from '@/hooks/useFilter'
import { getCreatedAt } from '@/utils/misc'

const emit = defineEmits(['searchEmit'])

const route = useRoute()
const selectedItem = ref(route.query.event)
const createdAt = ref(getCreatedAt(route.query.createdAt))
const email = ref(route.query.email)
const username = ref(route.query.username)
const myForm = ref(null)

const {
  submitBtnLoading,
  submit,
} = useFilter(emit)

const formSchema = yup.object({
  event: yup.string().nullable(),
  createdAt: yup.array().nullable(),
  username: yup.string().nullable(),
  email: yup.string().email().nullable(),
})


const resetFormValue = () => {
  myForm.value.setFieldValue('email', email.value)
  myForm.value.setFieldValue('username', username.value)
  myForm.value.setFieldValue('createdAt', createdAt.value)
  myForm.value.setFieldValue('event', selectedItem.value)
}

onMounted(async () => {
  resetFormValue()
})


const resetForm = () => {
  selectedItem.value = undefined
  username.value = undefined
  email.value = undefined
  createdAt.value = []
  resetFormValue()
  emit(
    'searchEmit',
    {
      reset: true,
    },
  )
}
</script>

<template>
  <Form
    ref="myForm"
    :validation-schema="formSchema"
    @submit="submit"
  >
    <VCard
      elevation="3"
      rounded="3"
      title="Filters"
    >
      <VCardText>
        <VRow>
          <VCol
            cols="12"
            sm="4"
          >
            <Field
              v-slot="{ field }"
              name="event"
              type="text"
            >
              <VSelect
                v-model="selectedItem"
                v-bind="field"
                label="請選擇事件"
                :items="userLogSelectItem"
                item-title="name"
                item-value="value"
                placeholder="請選擇事件"
                prepend-inner-icon="mdi-gesture-tap"
                variant="outlined"
                density="compact"
              />
            </Field>
            <ErrorMessage name="event" />
          </VCol>
          <VCol
            cols="12"
            sm="4"
          >
            <Field
              v-slot="{ field }"
              name="email"
              type="email"
            >
              <VTextField
                v-bind="field"
                v-model="email"
                label="Email"
                type="email"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-email"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="email"
            />
          </VCol>
          <VCol
            cols="12"
            sm="4"
          >
            <Field
              v-slot="{ field }"
              name="username"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="username"
                label="username"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-account"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="username"
            />
          </VCol>
          <VCol
            cols="12"
            sm="8"
          >
            <Field
              v-slot="{ field }"
              name="createdAt"
              type="text"
            >
              <DatePicker
                v-model:value="createdAt"
                v-bind="field"
                type="datetime"
                range
                value-type="format"
              >
                <template #input>
                  <VTextField
                    v-model="createdAt"
                    label="搜尋創建日期"
                    hide-details
                    variant="outlined"
                    density="compact"
                    readonly
                    placeholder="搜尋創建日期"
                    prepend-inner-icon="mdi-calendar-outline"
                  />
                </template>
                <template #icon-calendar />
              </DatePicker>
            </Field>
            <ErrorMessage name="date" />
          </VCol>

          <VCol
            cols="12"
            sm="2"
          >
            <v-btn
              block
              color="primary"
              type="submit"
              height="44"
            >
              Search
            </v-btn>
          </VCol>
          <VCol
            cols="12"
            sm="2"
          >
            <VBtn
              block
              color="error"
              type="reset"
              variant="outlined"
              height="44"
              @click.prevent="resetForm"
            >
              Reset
            </VBtn>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>
  </Form>
</template>
