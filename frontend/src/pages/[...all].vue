<script setup>
import OtherBase from '@/views/other/Base.vue'
import misc404 from '@images/pages/404.png'
</script>

<template>
  <OtherBase :img="misc404">
    <template #header>
      <ErrorHeader
        error-code="404"
        error-title="Page Not Found ⚠️"
        error-description="We couldn't find the page you are looking for."
      />
    </template>
  </OtherBase>
</template>
