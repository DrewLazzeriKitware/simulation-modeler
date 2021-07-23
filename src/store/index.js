import Vuex from "vuex";

import wslink from "simulation-modeler/src/store/wslink";
import simput from "simulation-modeler/src/store/simput";
import app from "simulation-modeler/src/store/app";
import viz from "simulation-modeler/src/store/viz";

function createStore() {
  return new Vuex.Store({
    modules: {
      wslink,
      simput,
      app,
      viz
    }
  });
}

export default createStore;
