import SmartConnect from "wslink/src/SmartConnect";
import vtkWSLinkClient from "vtk.js/Sources/IO/Core/WSLinkClient";
import { connectImageStream } from "vtk.js/Sources/Rendering/Misc/RemoteView";

import protocols from "simulation-modeler/src/protocols";

vtkWSLinkClient.setSmartConnectClass(SmartConnect);

export default {
  state: {
    client: null
  },
  getters: {
    WS_CLIENT(state) {
      return state.client;
    }
  },
  mutations: {
    WS_CLIENT_SET(state, value) {
      state.client = value;
    }
  },
  actions: {
    // Common
    async WS_RESET_CAMERA({ state }) {
      await state.client
        .getRemote()
        .modeler.resetCamera()
        .catch(console.error);
    },
    async WS_TOGGLE_EDGE_VISIBILITY({ state }) {
      await state.client
        .getRemote()
        .modeler.toggleEdgeVisibility()
        .catch(console.error);
    },
    async WS_TOGGLE_AXES_GRID_VISIBILITY({ state }) {
      await state.client
        .getRemote()
        .modeler.toggleGridAxesVisibility()
        .catch(console.error);
    },
    async WS_SET_VERTICAL_SPACE({ state }, zSpace) {
      await state.client
        .getRemote()
        .modeler.setVerticalSpace(zSpace)
        .catch(console.error);
    },
    async WS_SET_ELEVATION_SCALE({ state }, eScale) {
      await state.client
        .getRemote()
        .modeler.setElevationScale(eScale)
        .catch(console.error);
    },

    // ------------------------------------------------------------------------
    // WS initialization
    // ------------------------------------------------------------------------

    async WS_CONNECT({ commit, dispatch }) {
      const client = vtkWSLinkClient.newInstance();
      client.setProtocols(protocols);
      client.onConnectionError(httpReq => {
        const message =
          (httpReq && httpReq.response && httpReq.response.error) ||
          `Connection error`;
        console.error(message);
        console.log(httpReq);
      });
      client.onConnectionClose(httpReq => {
        const message =
          (httpReq && httpReq.response && httpReq.response.error) ||
          `Connection close`;
        console.error(message);
        console.log(httpReq);
      });

      const config = { application: "modeler" };

      // Custom setup for development (http:8080 / ws:1234)
      if (location.port === "8080") {
        // We suppose that we have dev server and that ParaView/VTK is running on port 1234
        config.sessionURL = `ws://${location.hostname}:1234/ws`;
      }

      await client.connect(config);
      // Setup image-stream so remote render window get images
      const session = client.getConnection().getSession();
      connectImageStream(session);

      // Capture ws client in the store
      commit("WS_CLIENT_SET", client);

      // Catch up with server state
      dispatch("WS_LOAD_SERVER_STATE");
    },
    async WS_LOAD_SERVER_STATE({ state, dispatch, commit }) {
      const serverState = await state.client
        .getRemote()
        .modeler.getState()
        .catch(console.error);
      if (serverState) {
        dispatch("SIMPUT_INIT", serverState.state);
        dispatch("SIMPUT_FILES_SET", serverState.files);
        commit("VIZ_VIEW_ID_SET", serverState.view);
      }
      return serverState;
    },
    async WS_SAVE({ state }, view) {
      await state.client
        .getRemote()
        .modeler.saveSimputView(view)
        .catch(console.error);
    },
    async WS_RUN({ state }) {
      await state.client
        .getRemote()
        .modeler.runParflow()
        .catch(console.error);
    }
  }
};
