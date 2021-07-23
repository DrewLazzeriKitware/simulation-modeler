import { mapActions } from "vuex";

import ViewSelector from "simulation-modeler/src/components/ViewSelector";
import Error from "simulation-modeler/src/components/Error";
import Overview from "simulation-modeler/src/components/Overview";
import Simput from "simulation-modeler/src/components/Simput";

export default {
  name: "App",
  components: {
    Overview,
    ViewSelector,
    Error,
    Simput
  },
  data: () => ({
    drawerOpen: true,
    tab: null,
    items: [
      {
        text: "Simulation",
        disabled: false
      },
      {
        text: "Forcing",
        disabled: false
      },
      {
        text: "Simput",
        disabled: false
      }
    ]
  }),
  mounted() {
    this.connect();
  },
  methods: {
    ...mapActions({
      connect: "WS_CONNECT",
      save: "SIMPUT_SAVE",
      run: "WS_RUN"
    })
  }
};
