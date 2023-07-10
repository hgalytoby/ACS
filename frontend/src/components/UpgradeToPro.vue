<template>
  <VBtn
    v-if="false"
    color="error"
    class="product-upgrade-to-pro"
    href="https://themeselection.com/item/materio-vuetify-vuejs-admin-template/"
    target="_blank"
    rel="noopener noreferrer"
  >
    Upgrade to Pro

    <VMenu
      open-on-hover
      activator="parent"
      offset="15"
      max-width="400px"
      :close-on-content-click="false"
      transition="slide-y-reverse-transition"
    >
      <VCard/>
    </VMenu>
  </VBtn>
</template>

<style lang="scss" scoped>
.product-upgrade-to-pro {
  position: fixed;

  // To keep upgrade to pro button on top of v-layout
  z-index: 999;
  inset-block-end: 5%;
  inset-inline-end: 79px;

  .v-application &.v-btn.v-btn--elevated {
    box-shadow: 0 1px 20px 1px rgb(var(--v-theme-error)) !important;

    &:hover {
      box-shadow: none !important;
    }
  }
}
</style>
