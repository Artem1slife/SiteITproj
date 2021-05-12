<template>
  <div class="content-wrapper">
    <section>
      <div class="container">
        <h1 class="ui-title-1">Home</h1>
        <!-- Fail load-->
        <div class="fail-list">
          <transition-group name="failList">
            <div class="fail-item" v-for="fail in failsForLoad" :key="fail.id">
              <div class="ui-card ui-card--shadow">
                <div class="fail-item__info">
                  <span class="button-close" @click="deleteFail(fail.id)"></span>
                </div>
                <div class="fail-item__content">
                  <div class="fail-item__header">
                    <span class="ui-title-2">{{ fail.title }} </span>
                  </div>
                </div>
              </div>
            </div>
          </transition-group>
        </div>
      </div>
      <div class="container">
        <form @submit.prevent="onSubmit">
          <!-- Fail title-->
          <div class="form-item" :class="{ errorInput: $v.failTitle.$error }">
            <input type="text" placeholder="What we will watch?" v-model="failTitle"
              @change="$v.failTitle.$touch()"
              :class="{ error: $v.failTitle.$error }"
            />
            <div class="error" v-if="!$v.failTitle.required">
              Title is required.
            </div>
          </div>
          <!-- SUBMIT-->
          <div class="button-list">
            <button
              class="button button--round button-primary"
              type="submit"
              :disabled="submitStatus === 'PENDING'"
            >
              <span v-if="loading">Loading...</span><span v-else>Send</span>
            </button>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
export default {
  data() {
    return {
      submitStatus: null,
      failTitle: "",
    };
  },
  // Vuelodate
  validations: {
    failTitle: {
      required,
    },
  },
  methods: {
    // Submit NEW fail (submit button)
    onSubmit() {
      // Initialize Vuelodate
      this.$v.$touch();
      // Invalid
      if (this.$v.$invalid) {
        console.log("ERROR");
        this.submitStatus = "ERROR";
        // Valid
      } else {
        // fail
        const fail = {
          title: this.failTitle,
        };
        this.$store
          .dispatch("newFail", fail)
          .then(() => {
            this.submitStatus = "OK";
          })
          .catch((err) => {
            this.submitStatus = err.message;
          });

        // Reset
        this.failTitle = "";
        // Reset $v (validate)
        this.$v.$reset();
      }
    },
    // Delete button
    deleteFail(id) {
      this.$store.dispatch("deleteFail", id).then(() => {
        console.log("fail deleted");
        this.$store.dispatch("loadFails");
      });
    },
  },
  computed: {
    // Load buttons
    failsForLoad() {
      return this.$store.getters.fails;
    },
    // Show loading status
    loading() {
      return this.$store.getters.loading;
    },
  },
};
</script>

<style scoped>
.option-list {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.option-list .what-watch--radio {
  margin-right: 12px;
}
.option-list input {
  margin-bottom: 0;
}
.option-list label {
  margin-right: 20px;
  margin-bottom: 0;
}
.option-list label:last-child {
  margin-right: 0;
}
.total-time {
  margin-bottom: 20px;
}
.time-title {
  display: block;
  margin-bottom: 6px;
}
.time-input {
  max-width: 80px;
  margin-right: 10px;
}
.tag-list {
  margin-bottom: 20px;
}
.ui-tag__wrapper {
  margin-right: 18px;
  margin-bottom: 10px;
}
.ui-tag__wrapper:last-child {
  margin-right: 0;
}
.ui-tag.used {
  background-color: #444ce0;
  color: #fff;
}
.ui-tag.used .button-close:before,
.ui-tag.used .button-close:after {
  background-color: #fff;
}
.ui-tag .button-close.active {
  transform: rotate(45deg);
}
.tag-list--menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.tag-add--input {
  margin-bottom: 0;
  margin-right: 10px;
  height: 42px;
}
.total-time p {
  margin-bottom: 6px;
}
.total-time span {
  margin-right: 16px;
}
.total-time .fail-input {
  max-width: 80px;
  margin-bottom: 28px;
  margin-right: 10px;
}
.button-list {
  display: flex;
  justify-content: flex-end;
}
.form-item .error {
  display: none;
  margin-bottom: 8px;
  font-size: 13.4px;
  color: #fc5c65;
}
.form-item.errorInput .error {
  display: block;
}
input.error {
  border-color: #fc5c65;
}
</style>


