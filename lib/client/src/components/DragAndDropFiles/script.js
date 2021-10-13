export default {
  name: 'DragNDropFiles',
  data: () => ({
    file: '',
    dragging: false,
  }),
  methods: {
    onChange(e) {
      var files = e.target.files || e.dataTransfer.files;

      if (!files.length) {
        this.dragging = false;
        return;
      }

      this.createFile(files[0]);
    },
    createFile(file) {
      this.file = file;
      this.dragging = false;
      this.$emit('uploaded', file);
    },
    removeFile() {
      this.file = '';
    },
  },
  computed: {
    extension() {
      return this.file ? this.file.name.split('.').pop() : '';
    },
  },
};
