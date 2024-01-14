<script setup>
import Create from '@/pages/member/create.vue'
import { useMemberStore } from '@/stores/member'

const route = useRoute()
const show = ref(false)
const memberStore = useMemberStore()
const memberInfo = reactive({})

onMounted(async () => {
  const member = await memberStore.member(route.params.id)

  Object.assign(memberInfo, member)
  show.value = true
})
</script>

<template>
  <div>
    <transition
      appear
      mode="out-in"
      name="animate__animated animate__bounce"
      enter-active-class="animate__fadeIn animate__fast"
      leave-active-class="animate__fadeOut animate__fast"
    >
      <Create
        v-if="show"
        :member-info="memberInfo"
      />
    </transition>
  </div>
</template>
