<template>
  <div>
    <b-alert
      :show="dismissCountDown"
      dismissible
      :variant=alertState
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
    >{{ message }}</b-alert>
  </div>
</template>

<script>
export default {
  name: "Alert",
  props: ['message', 'alertState'],
  data() {
    return {
      dismissSecs: 3,
      dismissCountDown: 0,
    }
  },
  methods: {
    countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
      },
      showAlert() {
        this.dismissCountDown = this.dismissSecs
      }
  }
}
</script>
