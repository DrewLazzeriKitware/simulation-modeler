export default session => ({
  getState() {
    return session.call("parflow.state.get", []);
  },
  saveSimputView(view) {
    return session.call("parflow.simput.save", [view]);
  },
  runParflow() {
    return session.call("parflow.simput.run", []);
  },

  // Common among vizualizations 
  resetCamera() {
    return session.call('parflow.viz.reset.camera', []);
  },
  toggleGridAxesVisibility() {
    return session.call('parflow.viz.axes.toggle', []);
  },
  toggleEdgeVisibility() {
    return session.call('parflow.viz.edge.toggle', []);
  },
  setVerticalSpace(zSpace) {
    return session.call('parflow.viz.space.set', [zSpace]);
  },
  setElevationScale(eScale) {
    return session.call('parflow.viz.elevation.set', [eScale]);
  },


});
