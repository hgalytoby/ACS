<script setup>
import DefaultLayoutWithVerticalNav from './components/DefaultLayoutWithVerticalNav.vue'
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
        <component
          :is="Component"
          :key="$route.fullPath"
        />
      </transition>
    </RouterView>
  </DefaultLayoutWithVerticalNav>
</template>

<style lang="scss">
// As we are using `layouts` plugin we need its styles to be imported
@use "@layouts/styles/default-layout";
</style>
