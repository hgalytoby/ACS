<script setup>
import BaseAuth from '@/views/pages/auth/Base.vue'
</script>

<template>
  <BaseAuth>
    <template #content>
      <RouterView v-slot="{ Component }">
        <transition
          appear
          mode="out-in"
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInLeft animate__faster"
          leave-active-class="animate__fadeOutRight animate__faster"
        >
          <component :is="Component" />
        </transition>
      </RouterView>
    </template>
  </BaseAuth>
</template>

<style lang='scss'>
@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translate3d(-10%, 0, 0);
  }

  to {
    opacity: 1;
    transform: none;
  }
}
@keyframes fadeOutRight {
  from {
    opacity: 1;
    transform: none;
  }

  to {
    opacity: 0;
    transform: translate3d(10%, 0, 0);
  }
}
</style>
