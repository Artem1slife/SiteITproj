import firebase from 'firebase/app'

import Fail from './failForAnalysis_help'

export default {
  state: {
    fails: []
  },
  mutations: {
    loadFails (state, payload) {
      state.fails = payload
    },
    newFail (state, payload) {
      state.fails.push(payload)
    },
    editFail (state, {id, title}) {
      const fail = state.fails.find(f => {
        return f.id === id
      })
      fail.title = title
    }
  },
  actions: {
    // Load all Fails
    async loadFails ({commit}) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const fail = await firebase.database().ref('fails').once('value')
        // Get value
        const fails = fail.val()
        // New array
        const failsArray = []
        // Get fail key (id)
        Object.keys(fails).forEach(key => {
          const f = fails[key]
          failsArray.push(
            new Fail(
              f.title,
              f.user,
              key
            )
          )
        })
        // Send mutation
        commit('loadFails', failsArray)

        commit('setLoading', false)
      } catch (error) {
        commit('setLoading', false)
        commit('setError', error.message)
        throw error
      }
    },
    // Create new Fail
    async newFail ({commit, getters}, payload) {
      commit('clearError')
      commit('setLoading', true)
      try {
        // Use helped class
        const newFail = new Fail(
          payload.title,
          getters.user.id
        )
        const fail = await firebase.database().ref('fails').push(newFail)
        // Send mutation
        commit('newFail', {
          ...newFail,
          id: fail.key
        })

        commit('setLoading', false)
      } catch (error) {
        commit('setLoading', false)
        commit('setError', error.message)
        throw error
      }
    },
    // Edit Fail (popup)
    async editFail ({commit}, {id, title}) {
      commit('clearError')
      commit('setLoading', true)
      try {
        // Update title
        await firebase.database().ref('fails').child(id).update({title})
        // Send mutation
        commit('editFail', {id, title})

        commit('setLoading', false)
      } catch (error) {
        commit('setLoading', false)
        commit('setError', error.message)
        throw error
      }
    },
    // Edit Fail (button)
    async deleteFail ({commit}, id) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await firebase.database().ref('fails').child(id).remove()

        commit('setLoading', false)
      } catch (error) {
        commit('setLoading', false)
        commit('setError', error.message)
        throw error
      }
    }
  },
  getters: {
    // Get user All Fails
    fails (state, getters) {
      return state.fails.filter(fail => {
        return fail.user === getters.user.id
      })
    },

  }
}
