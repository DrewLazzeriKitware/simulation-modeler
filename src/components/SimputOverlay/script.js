import { mapGetters } from "vuex";
import PropertyFactory from "simput/src/components/core/PropertyFactory";

export default {
  name: "SimputOverlay",
  components: {
    PropertyFactory
  },
  data: () => ({
    hiddenAttributes: {}
  }),
  props: {
    view: { type: String, required: true }
  },
  computed: {
    ...mapGetters({
      dataManager: "SIMPUT_DATAMANAGER"
    }),
    simputData() {
      if (this.dataManager) {
        const activeViewIndex = 0; // Assumes not dynamic view
        this.dataManager.activateView(this.view, activeViewIndex);
        return {
          propList: this.dataManager.getPropertyList(),
          viewData: this.dataManager.getActiveViewData()
        };
      }
      return {};
    }
  },
  methods: {
    updateViewData(newData) {
      this.dataManager.updateViewData(newData);
    },
    toggleHiding(property) {
      this.$set(
        this.hiddenAttributes,
        property.title,
        !this.hiddenAttributes[property.title]
      );
    },
    hidden(property) {
      return this.hiddenAttributes[property.title];
    }
  }
};
