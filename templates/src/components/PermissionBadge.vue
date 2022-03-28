<template>
  <b-badge :variant="colorVariant">
    {{ permissionTitle }}
  </b-badge>
</template>

<script>
export default {
  name: 'PermissionBadge',
  props: {
    colorVariant: {
      type: String,
      required: true,
    }, 
    permissionTitle: {
      type: String,
      required: true
    },
  },
}
</script>
