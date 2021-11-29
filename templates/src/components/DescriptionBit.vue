<template>
  <b-badge
    :content="tooltipContent"
    v-tippy="{arrow: true, arrowType: 'round', theme: 'google'}" 
    class="no-drag" :variant="badgeVariant">{{ text }}<b-icon-x-circle-fill size="sm" class="rem-button" @click="clickHandler(startIndex)" pill></b-icon-x-circle-fill></b-badge>
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
    suggested: {
      type: Boolean,
      required: false,
    }
  },
  computed: {
    badgeVariant() {
      // author is present <=> bit assigned 
      if (this.author) {
        return "primary"
      }

      if (this.suggested) {
        return "secondary" 
      }

      // not assigned, not suggested
      return "warning"
    },
    tooltipContent() {
      if (this.author) {
        return `<em>${this.author}</em> has used this bit of description`
      }
      
      if (this.suggested) {
        return 'This is an automatic suggestion'
      }

      return 'This description bit is not assigned'
    },
  }
}
</script>

<style scoped>
.rem-button {
  margin-left: 0.2rem;
  cursor: pointer;
}
</style>