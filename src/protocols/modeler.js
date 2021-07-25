export default session => ({
  getState() {
    return session.call("sim.state.get", []);
  },
  saveSimputView(view) {
    return session.call("sim.simput.save", [view]);
  },
  runParflow() {
    return session.call("sim.simput.run", []);
  },

  // Common among vizualizations
  resetCamera() {
    return session.call("sim.viz.reset.camera", []);
  },
  toggleGridAxesVisibility() {
    return session.call("sim.viz.axes.toggle", []);
  },
  toggleEdgeVisibility() {
    return session.call("sim.viz.edge.toggle", []);
  },
  setVerticalSpace(zSpace) {
    return session.call("sim.viz.space.set", [zSpace]);
  },
  setElevationScale(eScale) {
    return session.call("sim.viz.elevation.set", [eScale]);
  }
});
