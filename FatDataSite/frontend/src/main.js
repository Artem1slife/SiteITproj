import Vue from 'vue'
import Vuelidate from 'vuelidate'

import App from './App.vue'
import router from './routes'
import store from './store'

import './assets/main.scss'

import firebase from 'firebase/app'
import 'firebase/auth'
import 'firebase/database'
import 'firebase/messaging'
import 'firebase/storage'

Vue.config.productionTip = false

Vue.use(
  Vuelidate
)

new Vue({
  router,
  store,
  render: h => h(App),
  created() {
    // Your web app's Firebase configuration
    var firebaseConfig = {
      apiKey: 'AIzaSyCBlG_g1TaNtFxCMDNMAsXC1ijPyDBjgpQ',
      authDomain: 'clever-analitics-text-22ccd.firebaseapp.com',
      databaseURL: 'https://clever-analitics-text-22ccd-default-rtdb.firebaseio.com',
      projectId: 'clever-analitics-text-22ccd',
      storageBucket: 'clever-analitics-text-22ccd.appspot.com',
      messagingSenderId: '384783073635',
      appId: '1:384783073635:web:f512219aefc67aa90c5356'
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);

    // Auth Check
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        // Check Logged
        this.$store.dispatch('loggedUser', user)
      }
       // Loading All Fails
       this.$store.dispatch('loadFails')
    })
  }


}).$mount('#app')