import PropertyFactory from "simput/src/components/core/PropertyFactory";

export default {
  name: "VariableTableProperty",
  props: {
    viewData: {
      required: true
    },
    prop: {
      required: true
    }
  },
  components: { PropertyFactory },
  methods: {
    updateTable() {
      // Value is bound by component, but trigger table reactivity and hooks
      this.$emit("change", this.prop.data);
    },
    labelForHeader(header) {
      if (this.prop.ui.domain.table_labels[header]) {
        return this.prop.ui.domain.table_labels[header];
      }
      if (this.prop.ui.id === header) {
        return this.prop.ui.label;
      }
      // FIXME can't find labels for variable_columns unless table has rows
      const matchingColumn = this.prop.ui.domain.columns.find(
        column => column.id === header
      );
      if (matchingColumn) {
        return matchingColumn.label;
      }
      return header;
    }
  },
  computed: {
    tableValue() {
      return this.prop.data.value[0];
    },
    columnOrder() {
      const order = this.prop.ui.domain.table_order;
      const columns = this.prop.ui.domain.columns.map(c => c.id);
      columns.sort((first, second) => {
        if (!order[first] && !order[second]) return 0;
        if (order[first] && !order[second]) return -1;
        if (!order[first] && order[second]) return 1;
        if (order[first] > order[second]) return 1;
        if (order[first] < order[second]) return -1;
        return 0;
      });
      return columns;
    },
    variableHeaders() {
      const headers = Object.keys(this.prop.ui.domain.variable_columns);
      return headers.map(this.labelForHeader);
    },
    columnHeaders() {
      const headers = this.columnOrder;
      return headers.map(this.labelForHeader);
    },
    isVisible() {
      return (
        this.prop.show(this.viewData) && this.prop.ui.domain.columns.length
      );
    }
  },
  beforeMount() {
    const update = () => this.$nextTick(this.$forceUpdate);
    this.unsubscribe = this.$store.getters.SIMPUT_DATAMANAGER.subscribe(
      update
    ).unsubscribe;
  },
  beforeDestroy() {
    this.unsubscribe();
  }
};
