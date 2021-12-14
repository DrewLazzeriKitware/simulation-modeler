export default {
  name: 'SimputItem',
  props: {
    itemId: {
      type: String,
    },
  },
  data() {
    return {
      data: null,
      domains: null,
    };
  },
  created() {
    this.onConnect = () => {
      this.update();
    };
    this.onChange = ({ id }) => {
      /* eslint-disable eqeqeq */
      if (id && this.itemId == id) {
        this.data = this.getSimput().getData(id);
        this.domains = this.getSimput().getDomains(id);
      }
      this.update();
    };
    this.simputChannel.$on('connect', this.onConnect);
    this.simputChannel.$on('change', this.onChange);
  },
  beforeUnmount() {
    this.simputChannel.$off('connect', this.onConnect);
    this.simputChannel.$off('change', this.onChange);
  },
  watch: {
    itemId() {
      this.update();
    },
  },
  computed: {
    available() {
      return !!(this.data && this.domains);
    },
    properties() {
      return this.data?.properties;
    },
    all() {
      const { data, domains, properties } = this;
      return {
        id: this.itemId,
        data,
        domains,
        properties,
      };
    },
  },
  methods: {
    update() {
      console.log('Updating');
      this.data = null;
      if (this.itemId) {
        this.data = this.getSimput().getData(this.itemId);
        this.domains = this.getSimput().getDomains(this.itemId);
      }
    },
    dirty(name) {
      this.simputChannel.$emit('dirty', { id: this.data.id, name });
    },
  },
  inject: ['simputChannel', 'getSimput'],
};
