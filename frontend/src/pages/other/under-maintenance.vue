<script setup>
import OtherBase from '@/views/other/Base.vue'
import underMaintenance from '@images/pages/under-maintenance.png'
</script>

<template>
  <OtherBase :img="underMaintenance">
    <template #header>
      <ErrorHeader
        error-title="Under Maintenance! 🚧"
        error-description="Sorry for the inconvenience but we're performing some maintenance at the moment"
      />
    </template>
  </OtherBase>
</template>
