<template>
    <div class="wrapper-content wrapper-content--fixed">
    <section>
        <div class="container">
            <div class="auth">
                <div class="auth__banner">
                    <h1 class="title">Hello banner</h1>
                    <img src="@/images/temp.png">
                </div>
                <div class="auth__form">
                    <span class="title">Login</span>
                    <form @submit.prevent="onSubmit">
                        <div class="form-item" :class="{ errorInput: $v.email.$error }">
                            <input type="email" placeholder="Email" v-model="email" :class="{ error: $v.email.$error }" @change="$v.email.$touch()"/>
                            <div class="error" v-if="!$v.email.required">Field is required</div>
                            <div class="error" v-if="!$v.email.email">Email is not correct</div>
                        </div>
                        <div class="form-item" :class="{ errorInput: $v.password.$error }">
                            <input type="password" placeholder="Password" v-model="password" :class="{ error: $v.password.$error }" @change="$v.password.$touch()"/>
                            <div class="error" v-if="!$v.password.required">Password is required.</div>
                            <div class="error" v-if="!$v.password.minLength">Password must have at least {{ $v.password.$params.minLength.min }} letters.</div>
                        </div>
                        <div class="buttons-list">
                            <button class="btn btnPrimary" type="submit" :disabled="submitStatus === 'PENDING'">Login</button>
                        </div>
                        <div class="buttons-list buttons-list--info">
                            <p class="" v-if="submitStatus === 'OK'">Thanks for your submission!</p>
                            <p class="" v-if="submitStatus === 'ERROR'">Please fill the form correctly.</p>
                            <p class="" v-if="submitStatus === 'PENDING'">Sending...</p>
                        </div>
                        <div class="buttons-list buttons-list--info">
                            <span>Need Registration?<router-link to="/registration"> Enter Here</router-link></span>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
    </div>
</template>

<script>
import { required, email, minLength } from 'vuelidate/lib/validators'
export default {
  data () {
    return {
      email: '',
      password: '',
      repeatPassword: '',
      submitStatus: null
    }
  },
  // Vuelidate
  validations: {
    email: {
      required,
      email
    },
    password: {
      required,
      minLength: minLength(6)
    }
  },
  methods: {
    // Login button
    onSubmit () {
      // Initialize Vuelodate
      this.$v.$touch()
      // Invalid
      if (this.$v.$invalid) {
        this.submitStatus = 'ERROR'
      // Valid
      } else {
        // User
        const user = {
          email: this.email,
          password: this.password
        }
        this.$store.dispatch('loginUser', user)
          .then(() => {
            this.submitStatus = 'OK'
            this.$router.push('/aboutCat')
          })
          .catch(err => {
            this.submitStatus = err.message
          })
      }
    }
  },
  computed: {
    // Show loading status
    loading () {
      return this.$store.getters.loading
    }
  }
}
</script>

<style scoped>
.auth {
  display: flex;
}
.auth__banner,
.auth__form {
  width: 50%;
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
  animation: shake 0.3s;
}
.buttons-list {
  text-align: right;
  margin-bottom: 20px;
}
.buttons-list.buttons-list--info {
  text-align: center;
}
.buttons-list.buttons-list--info:last-child {
  margin-bottom: 0;
}
a {
  color: #444ce0;
}



</style>