<script setup>
import DefaultLayoutWithVerticalNav from './components/DefaultLayoutWithVerticalNav.vue'
</script>

<template>
  <transition
    appear
    mode="out-in"
    name="anime-speed animate__animated animate__bounce"
    enter-active-class="animate__fadeIn"
    leave-active-class="animate__fadeOut"
  >
    <DefaultLayoutWithVerticalNav>
      <vue-progress-bar/>
      <RouterView/>
    </DefaultLayoutWithVerticalNav>
  </transition>
</template>

<style lang="scss">
// As we are using `layouts` plugin we need its styles to be imported
@use "@layouts/styles/default-layout";
</style>
