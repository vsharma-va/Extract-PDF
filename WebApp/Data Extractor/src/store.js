import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

export const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      paths: ["csvString"],
      storage: window.sessionStorage,
    })
  ],
  state: {
    csvString: '',
  }
})