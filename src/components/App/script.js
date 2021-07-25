import { mapActions, mapGetters } from "vuex";

import Error from "simulation-modeler/src/components/Error";
import Simput from "simulation-modeler/src/components/Simput";
import RemoteRenderView from "simulation-modeler/src/components/RemoteRenderView";
import ViewControl from "simulation-modeler/src/components/ViewControl";

export default {
  name: "App",
  components: {
    Error,
    Simput,
    RemoteRenderView,
    ViewControl
  },
  data: () => ({
    drawerOpen: true,
    tab: null,
    items: [
      {
        text: "Grid",
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
    ...mapGetters({
      client: "WS_CLIENT",
      viewId: "VIZ_VIEW_ID"
    }),
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
