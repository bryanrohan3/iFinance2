// way of keeping data for a long period of time
import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    authToken: null,
    userProfile: null,
    expenses: [],
  },
  getters: {
    getAuthToken(state) {
      return state.authToken;
    },
    getUserProfile(state) {
      return state.userProfile;
    },
  },
  mutations: {
    setAuthToken(state, token) {
      state.authToken = token;
    },

    setExpenses(state, expenses) {
      state.expenses = expenses;
    },

    setUserProfile(state, user) {
      state.userProfile = user;
    },
    logout(state) {
      state.authToken = null;
      state.userProfile = null;
    },
    setBankBalance(state, balance) {
      state.userProfile.bank_balance = balance;
    },
  },
  actions: {},
  plugins: [createPersistedState()],
});
