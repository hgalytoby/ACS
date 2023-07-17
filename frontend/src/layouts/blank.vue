<template>
  <div class="layout-wrapper layout-blank">
    <vue-progress-bar />
    <RouterView />
  </div>
</template>

<style>
.layout-wrapper.layout-blank {
  flex-direction: column;
}
</style>
