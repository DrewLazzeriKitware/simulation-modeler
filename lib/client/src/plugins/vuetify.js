import "@mdi/font/css/materialdesignicons.css";
import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: "mdi",
    values: {
      navigationBackward: "mdi-chevron-left",
      navigationForward: "mdi-chevron-right"
    }
  }
});
