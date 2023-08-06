<script setup>
import { userLogSelectItem } from '@/utils/filter-select-item'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import DatePicker from 'vue-datepicker-next'


const emit = defineEmits(['searchEmit'])

const formSchema = yup.object({
  event: yup.string().nullable(),
})

const submitBtnLoading = ref(false)
const selectedItem = ref(null)
const date = ref([])

const submit = payload => {
  submitBtnLoading.value = true
  emit('searchEmit', payload)
  submitBtnLoading.value = false
}

const t = ref([])

const resetForm = () => {
  selectedItem.value = null
  emit('searchEmit', {})
}
</script>

<template>
  <Form
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
            sm="3"
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
            sm="5"
          >
            <DatePicker
              v-model:value="date"
              type="datetime"
              range
              value-type="format"
            >
              <template #input>
                <VTextField
                  v-model="date"
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

<style lang='scss'>
.account-settings-log-date-picker {
  position: absolute;
  bottom: 22px;
  z-index: -9999 !important;
}
</style>
