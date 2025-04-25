<script setup>
import { bloodTypeSelectItem } from '@/utils/filter-select-item'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import DatePicker from 'vue-datepicker-next'
import useFilter from '@/hooks/useFilter'
import { getMemberListFilterFormItems } from '@/utils/filter-form-items'

const emit = defineEmits(['searchEmit'])

const formSchema = yup.object({
  name: yup.string().nullable(),
  bloodType: yup.string().nullable(),
  phone: yup.string().nullable(),
  company: yup.string().nullable(),
  jobTitle: yup.string().nullable(),
  createdAt: yup.array().nullable(),
})

const initItems = {
  name: undefined,
  bloodType: undefined,
  phone: undefined,
  company: undefined,
  jobTitle: undefined,
  createdAt: [],
}

const formItems = reactive(getMemberListFilterFormItems())

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
              name="name"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.name"
                label="Name"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-account-outline"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="name"
            />
          </VCol>
          <VCol
            cols="15"
            sm="2"
          >
            <Field
              v-slot="{ field }"
              name="bloodType"
              type="text"
            >
              <VSelect
                v-model="formItems.bloodType"
                v-bind="field"
                label="請選擇血型"
                :items="bloodTypeSelectItem"
                item-title="name"
                item-value="value"
                placeholder="請選擇血型"
                prepend-inner-icon="mdi-ab-testing"
                variant="outlined"
                density="compact"
              />
            </Field>
            <ErrorMessage name="bloodType" />
          </VCol>
          <VCol
            cols="15"
            sm="2"
          >
            <Field
              v-slot="{ field }"
              name="phone"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.phone"
                label="Phone"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-phone-outline"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="phone"
            />
          </VCol>
          <VCol
            cols="15"
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="company"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.company"
                label="Company"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-domain"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="company"
            />
          </VCol>
          <VCol
            cols="15"
            sm="2"
          >
            <Field
              v-slot="{ field }"
              name="jobTitle"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.jobTitle"
                label="JobTitle"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-card-account-details-outline"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="jobTitle"
            />
          </VCol>
          <VCol
            cols="12"
            sm="5"
          >
            <Field
              v-slot="{ field }"
              name="birthday"
              type="text"
            >
              <DatePicker
                v-model:value="formItems.birthday"
                v-bind="field"
                type="datetime"
                range
                value-type="format"
              >
                <template #input>
                  <VTextField
                    v-model="formItems.birthday"
                    label="Birthday"
                    hide-details
                    variant="outlined"
                    density="compact"
                    readonly
                    placeholder="Birthday"
                    prepend-inner-icon="mdi-calendar-outline"
                  />
                </template>
                <template #icon-calendar />
              </DatePicker>
            </Field>
            <ErrorMessage
              class="error-message"
              name="birthday"
            />
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
            sm="1"
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
            sm="1"
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
