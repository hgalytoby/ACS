<template>
  <transition
    appear
    mode="out-in"
    name="layout-anime-speed animate__animated animate__bounce"
    enter-active-class="animate__fadeIn"
    leave-active-class="animate__fadeOut"
  >
    <div class="layout-wrapper layout-blank">
      <vue-progress-bar/>
      <RouterView/>
    </div>
  </transition>
</template>

<style>
.layout-wrapper.layout-blank {
  flex-direction: column;
}
</style>
