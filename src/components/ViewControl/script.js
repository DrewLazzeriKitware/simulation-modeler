import { mapGetters, mapActions } from "vuex";

export default {
  name: "ViewControl",
  data: () => ({
    vertical: 1,
    elevation: 0,
    showEdges: false,
    showGridAxes: false
  }),
  computed: {
    ...mapGetters({
      viz: "VIZ_NAME"
    })
  },
  methods: {
    ...mapActions({
      setVerticalSpace: "VIZ_UPDATE_VERTICAL_SPACE",
      setElevationScale: "VIZ_UPDATE_ELEVATION_SCALE",
      resetCamera: "VIZ_RESET_CAMERA",
      toggleGridAxesVisibility: "VIZ_TOGGLE_AXES_GRID_VISIBILITY",
      toggleEdgeVisibility: "VIZ_TOGGLE_EDGE_VISIBILITY"
    }),
    expandVertical() {
      this.vertical += 3;
    },
    compressVertical() {
      this.vertical = 1;
    },
    expandElevation() {
      this.elevation += 3;
    },
    compressElevation() {
      this.elevation = 0;
    },
    toggleEdges() {
      this.showEdges = !this.showEdges;
      this.toggleEdgeVisibility();
    },
    toggleGridAxes() {
      this.showGridAxes = !this.showGridAxes;
      this.toggleGridAxesVisibility();
    }
  },
  watch: {
    vertical(zScale) {
      this.setVerticalSpace(zScale);
    },
    elevation(eScale) {
      this.setElevationScale(eScale);
    }
  }
};
