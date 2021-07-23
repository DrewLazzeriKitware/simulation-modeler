import Vue from "vue";
import Vuex from "vuex";
import Vuetify from "vuetify";

import "vuetify/dist/vuetify.min.css";
import "typeface-roboto";

import App from "simulation-modeler/src/components/App";

import store from "simulation-modeler/src/store";
import icons from "simulation-modeler/src/plugins/icons";

Vue.config.productionTip = false;
Vue.use(Vuex);
Vue.use(Vuetify, icons);

new Vue({
  store,
  render: h => h(App)
}).$mount("#app");
