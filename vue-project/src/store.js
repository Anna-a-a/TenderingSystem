// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    user_type: null,
  },
  mutations: {
    setUserType(state, userType) {
      state.user_type = userType;
    },
  },
  actions: {
    async fetchUserType({ commit }) {
      try {
        const response = await fetch('/user_type');
        const data = await response.json();
        commit('setUserType', data.user_type);
      } catch (error) {
        console.error(error);
      }
    },
  },
});
