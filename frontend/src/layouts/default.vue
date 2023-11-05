<script setup>
import DefaultLayoutWithVerticalNav from './components/DefaultLayoutWithVerticalNav.vue'
import { useRoute } from 'vue-router'
import 'vue-datepicker-next/index.css'
import { connectWebSocket } from '@/utils/websocket'

const route = useRoute()

connectWebSocket()
</script>

<template>
  <DefaultLayoutWithVerticalNav>
    <vue-progress-bar />
    <RouterView v-slot="{ Component }">
      <transition
        appear
        mode="out-in"
        name="animate__animated animate__bounce"
        enter-active-class="animate__fadeIn animate__faster"
        leave-active-class="animate__fadeOut animate__faster"
      >
        <component :is="Component" />
      </transition>
    </RouterView>
  </DefaultLayoutWithVerticalNav>
</template>

<style lang="scss">
// As we are using `layouts` plugin we need its styles to be imported
@use "@layouts/styles/default-layout";
@import '@styles/date-picker';
</style>
