export default {
  state: {
    name: "grid",
    viewId: "0"
  },
  getters: {
    VIZ_VIEW_ID(state) {
      return state.viewId;
    },
    VIZ_NAME(state) {
      return state.name;
    }
  },
  mutations: {
    VIZ_VIEW_ID_SET(state, value) {
      state.viewId = value;
    },
    VIZ_NAME_SET(state, value) {
      state.name = value;
    }
  },
  actions: {
    VIZ_RESET_CAMERA({ dispatch }) {
      dispatch("WS_RESET_CAMERA");
    },
    VIZ_TOGGLE_DARK_MODE({ dispatch }) {
      dispatch("WS_TOGGLE_DARK_MODE");
    },
    VIZ_UPDATE_VERTICAL_SPACE({ dispatch }, space) {
      dispatch("WS_SET_VERTICAL_SPACE", space);
    },
    VIZ_UPDATE_ELEVATION_SCALE({ dispatch }, scale) {
      dispatch("WS_SET_ELEVATION_SCALE", scale);
    },
    VIZ_TOGGLE_EDGE_VISIBILITY({ dispatch }) {
      dispatch("WS_TOGGLE_EDGE_VISIBILITY");
    },
    VIZ_TOGGLE_AXES_GRID_VISIBILITY({ dispatch }) {
      dispatch("WS_TOGGLE_AXES_GRID_VISIBILITY");
    },
    VIZ_ACTIVATE({ dispatch, commit }, name) {
      commit("VIZ_NAME_SET", name);
      dispatch("WS_ACTIVATE_VISUALIZATION", name);
    }
  }
};
