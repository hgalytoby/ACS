<script setup>
const props = defineProps({
  item: {
    type: null,
    required: true,
  },
})

const isCardDetailsVisible = ref(false)
</script>

<template>
  <li
    class="nav-link"
    :class="{ disabled: false }"
    @click="isCardDetailsVisible = !isCardDetailsVisible"
  >
    <a>
      <VIcon
        :icon="item.icon"
        class="nav-item-icon"
      />
      <span class="nav-item-title">
        {{ item.title }}
      </span>
      <VBtn
        variant="text"
        icon
        color="secondary"
      >
        <VIcon :icon="!isCardDetailsVisible ? 'mdi-chevron-right' : 'mdi-chevron-down'" />
      </VBtn>
    </a>
  </li>
  <VExpandTransition>
    <div v-show="isCardDetailsVisible">
      <slot />
    </div>
  </VExpandTransition>
</template>

<style lang='scss'>
.layout-vertical-nav {
  .nav-link a {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
}
</style>
