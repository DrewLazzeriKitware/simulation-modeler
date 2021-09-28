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
      if (!file.type.match('text.*')) {
        alert('please select txt file');
        this.dragging = false;
        return;
      }

      if (file.size > 5000000) {
        alert('please check file size no over 5 MB.');
        this.dragging = false;
        return;
      }

      this.file = file;
      console.log(this.file);
      this.dragging = false;
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
