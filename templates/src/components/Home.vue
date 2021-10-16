<template>
  <b-container fluid>
    <div class="container">
      <button type="button" class="btn btn-primary">Import text</button>
      <button type="button" class="btn btn-primary">Upload image</button>

      <b-row>
        <b-col sm="1">
          <button type="button" class="btn btn-primary">Select words</button>
        </b-col>
        <b-col sm="5">
          <b-form-textarea
            id="textarea-auto-height"
            placeholder="Auto height textarea"
            rows="3"
            max-rows="8"
          ></b-form-textarea>
        </b-col>
      </b-row>
      
    </div>
  </b-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  data() {
    return {
      msg: "",
      text: "",
    };
  },
  methods: {
    // getMessage() {
    //   axios.get(this.$hostname)
    //     .then((res) => {
    //       this.msg = res.data
    //     })
    //     .catch((error) => {
    //       console.error(error) // TODO: handle error correctly
    //     })
    // },
  },
  created() {
    // this.getMessage()
  },
};
</script>