export default {
  name: "SimulationType",
  props: {
    shortcuts: { type: Object, default: () => ({}) }
  },
  mounted() {
    window.comp = this;
  }
};
