<script setup>
import { systemLogSelectItem } from '@/utils/filter-select-item'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import DatePicker from 'vue-datepicker-next'
import useFilter from '@/hooks/useFilter'
import { getSystemLogFilterFormItems } from '@/utils/filter-form-items'

const emit = defineEmits(['searchEmit'])

const formSchema = yup.object({
  event: yup.string().nullable(),
  createdAt: yup.array().nullable(),
})

const initItems = {
  event: undefined,
  createdAt: [],
}

const formItems = reactive(getSystemLogFilterFormItems())

const {
  myForm,
  resetForm,
  submit,
} = useFilter(emit, formItems, initItems)
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
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="event"
              type="text"
            >
              <VSelect
                v-model="formItems.event"
                v-bind="field"
                label="請選擇事件"
                :items="systemLogSelectItem"
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
            <Field
              v-slot="{ field }"
              name="createdAt"
              type="text"
            >
              <DatePicker
                v-model:value="formItems.createdAt"
                v-bind="field"
                type="datetime"
                range
                value-type="format"
              >
                <template #input>
                  <VTextField
                    v-model="formItems.createdAt"
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
