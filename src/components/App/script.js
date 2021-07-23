import { mapActions } from "vuex";

import Error from "simulation-modeler/src/components/Error";
import Simput from "simulation-modeler/src/components/Simput";

export default {
  name: "App",
  components: {
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
  computed: {
    selectedTabText() {
      return this.items[this.tab] && this.items[this.tab].text;
    }
  },
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
