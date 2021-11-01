<template>
  <div>
    <div class="container">
      <b-alert
        :show="dismissCountDown"
        dismissible
        :variant=state
        @dismissed="dismissCountDown=0"
        @dismiss-count-down="countDownChanged"
      >{{ message }}
      </b-alert>
    </div>
  </div>
</template>

<script>
export default {
  name: "Alert",
  data() {
    return {
      message: '',
      state: '',
      dismissSecs: 3,
      dismissCountDown: 0,
    }
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    showSuccessAlert(message) {
      this.message = message
      this.state = 'success'
      this.dismissCountDown = this.dismissSecs
    },
    showWarningAlert(message) {
      this.message = message
      this.state = 'danger'
      this.dismissCountDown = this.dismissSecs
    }
  },
  created() {
    this.$root.$refs.Alert = this
  }
}
</script>
