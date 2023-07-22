<script setup>
import OtherBase from '@/views/other/Base.vue'
import misc401 from '@images/pages/401.png'
</script>

<template>
  <OtherBase :img="misc401">
    <template #header>
      <ErrorHeader
        error-code="401"
        error-title="You are not authorized! 🔐"
        error-description="You don't have permission to access this page. Go Home!"
      />
    </template>
  </OtherBase>
</template>
