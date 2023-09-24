<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import DatePicker from 'vue-datepicker-next'
import useFilter from '@/hooks/useFilter'
import { getMemberRecordListFilterFormItems } from '@/utils/filter-form-items'
import { statusSelectItem } from '@/utils/filter-select-item'

const emit = defineEmits(['searchEmit'])

const formSchema = yup.object({
  status: yup.string().nullable(),
  memberLocationName: yup.string().nullable(),
  memberName: yup.string().nullable(),
  memberPhone: yup.string().nullable(),
  memberCompany: yup.string().nullable(),
  memberJobTitle: yup.string().nullable(),
  createdAt: yup.array().nullable(),
})

const initItems = {
  status: undefined,
  memberLocationName: undefined,
  memberName: undefined,
  memberPhone: undefined,
  memberCompany: undefined,
  memberJobTitle: undefined,
  createdAt: [],
}

const formItems = reactive(getMemberRecordListFilterFormItems())

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
            cols="15"
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="memberName"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.memberName"
                label="MemberName"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-account-outline"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="memberName"
            />
          </VCol>
          <VCol
            cols="15"
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="memberPhone"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.memberPhone"
                label="MemberPhone"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-phone-outline"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="memberPhone"
            />
          </VCol>
          <VCol
            cols="15"
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="memberCompany"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.memberCompany"
                label="MemberCompany"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-domain"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="memberCompany"
            />
          </VCol>
          <VCol
            cols="15"
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="memberJobTitle"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.memberJobTitle"
                label="MemberJobTitle"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-card-account-details-outline"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="memberJobTitle"
            />
          </VCol>
          <VCol
            cols="12"
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="memberLocationName"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="formItems.memberLocationName"
                label="LocationName"
                type="text"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-map-marker-outline"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="memberLocationName"
            />
          </VCol>
          <VCol
            cols="15"
            sm="3"
          >
            <Field
              v-slot="{ field }"
              name="status"
              type="text"
            >
              <VSelect
                v-model="formItems.status"
                v-bind="field"
                label="請選擇進出入狀態"
                :items="statusSelectItem"
                item-title="name"
                item-value="value"
                placeholder="進出入狀態"
                prepend-inner-icon="mdi-exit-run"
                variant="outlined"
                density="compact"
              />
            </Field>
            <ErrorMessage name="status" />
          </VCol>
          <VCol
            cols="12"
            sm="4"
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
            <ErrorMessage
              class="error-message"
              name="createdAt"
            />
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
