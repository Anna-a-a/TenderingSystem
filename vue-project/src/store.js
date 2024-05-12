import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state() {
    return {
      userTypeVuex: null,
    };
  },
  mutations: {
    SET_USER_TYPE(state, userTypeVuex) {
      state.userTypeVuex = userTypeVuex;
    },
  },
  actions: {
    async getUserTypeVuex({ commit }) {
      try {
        const response = await axios.get('/user_info');
        commit('SET_USER_TYPE', response.data.user_type);
      } catch (error) {
        console.error(error);
      }
    },
  },
});

export default store;
