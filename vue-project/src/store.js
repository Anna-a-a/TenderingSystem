// store.js

import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      isAuthenticated: false,
    };
  },
  mutations: {
    setAuthentication(state, value) {
      state.isAuthenticated = value;
    },
  },
});

export default store;
