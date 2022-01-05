<template>
  <div>
    <!-- Not loading, display button -->
    <b-button 
      v-if="progress === -1" 
      :disabled="progress !== -1" 
      @click="handleClick"
      variant="primary">
      <slot></slot>
    </b-button>
    <!-- Loading, display progress bar-->
    <b-progress class="progress-bar" :value="progress" show-progress :max="100" v-else/>
  </div>
</template>

<script>
export default {
  name: 'WaitingButton',
  props: {
    // indicates the progress of the loading action; -1 if no loading currently
    progressPercentage: {
      type: Number,
      required: true,
    },
    // the action that beings the loading
    startAction: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      progress: 0,
    }
  },
  methods: {
    handleClick() {
      this.progress = 0
      this.startAction()
    },
  },
  mounted() {
    this.progress = this.progressPercentage
  },
}
</script>

<style scoped>
.progress-bar {
  width: 25%;
  margin-left: auto;
  margin-right: auto;
}
</style>