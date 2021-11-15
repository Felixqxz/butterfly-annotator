<template>
  <b-badge variant="primary">{{ text }}<b-icon-x-circle-fill size="sm" class="rem-button" @click="clickHandler(startIndex)" pill></b-icon-x-circle-fill></b-badge>
</template>

<script>
export default {
  name: 'DescriptionBit',
  props: {
    text: {
      type: String,
      required: true,
    },
    startIndex: {
      type: Number,
      required: true,
    },
    clickHandler: {
      type: Function,
      required: true,
    },
  },
}
</script>

<style scoped>
.rem-button {
  margin-left: 0.2rem;
  cursor: pointer;
}
</style>