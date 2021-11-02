<template>
  <b-badge :variant="colorVariant">
    {{ permissionTitle }}
  </b-badge>
</template>

<script>
export default {
  name: 'PermissionBadge',
  props: ['colorVariant', 'permissionTitle']
}
</script>
