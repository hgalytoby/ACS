<script setup>
import { useTheme } from 'vuetify'
import authV1MaskDark from '@images/pages/auth-v1-mask-dark.png'
import authV1MaskLight from '@images/pages/auth-v1-mask-light.png'
import authV1Tree2 from '@images/pages/auth-v1-tree-2.png'
import authV1Tree from '@images/pages/auth-v1-tree.png'
import { useRoute } from 'vue-router'

const vuetifyTheme = useTheme()
const route = useRoute()

const authThemeMask = computed(() => {
  return vuetifyTheme.global.name.value === 'light' ? authV1MaskLight : authV1MaskDark
})
</script>

<template>
  <div class="auth-wrapper d-flex align-center justify-center pa-4">
    <RouterView v-slot="{ Component }">
      <transition
        appear
        mode="out-in"
        name="animate__animated animate__bounce"
        enter-active-class="animate__fadeInLeft animate__faster"
        leave-active-class="animate__fadeOutRight animate__faster"
      >
        <component
          :is="Component"
          :key="$route.fullPath"
        />
      </transition>
    </RouterView>

    <VImg
      class="auth-footer-start-tree d-none d-md-block"
      :src="authV1Tree"
      :width="250"
    />

    <VImg
      :src="authV1Tree2"
      class="auth-footer-end-tree d-none d-md-block"
      :width="350"
    />

    <!-- bg img -->
    <VImg
      class="auth-footer-mask d-none d-md-block"
      :src="authThemeMask"
    />
  </div>
</template>

<style lang='scss'>
@use "@core/scss/pages/page-auth.scss";
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
