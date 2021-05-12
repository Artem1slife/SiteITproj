import Vue from 'vue'
import Vuex from 'vuex'

import user from './user'
import fail from './failForAnalysis'
import common from './common'

import Uimini from 'uimini/dist/css/uimini.css'

Vue.use(
  Vuex,
  Uimini,
  )

export default new Vuex.Store({
  modules: {
    user,
    fail,
    common,
  }
})