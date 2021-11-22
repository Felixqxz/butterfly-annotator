<template>
  <b-badge
    :content="author ? `<em>${author}</em> has used this bit of description` : 'This description bit is not assigned'"
    v-tippy="{arrow: true, arrowType: 'round', theme: 'google'}" 
    class="no-drag" variant="primary">{{ text }}<b-icon-x-circle-fill size="sm" class="rem-button" @click="clickHandler(startIndex)" pill></b-icon-x-circle-fill></b-badge>
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
    author: { // the author of the final annotation (ie with the polygon)
      type: String,
      required: false,
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