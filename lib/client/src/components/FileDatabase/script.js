import DragAndDropFiles from '../DragAndDropFiles';

export default {
  name: 'FileDatabase',
  components: {
    DragAndDropFiles,
  },
  props: ['files', 'value'],
  data: () => ({ searchQuery: '', fileStats: {} }),
  methods: {
    iconFromType(type) {
      if (type === 'zip') return 'mdi-folder-zip';
      if (type === 'folder') return 'mdi-folder';
      return 'mdi-file';
    },
    searchMatch(file) {
      if (this.searchQuery === '') return true;
      const regex = new RegExp(this.searchQuery);
      const checks = [
        file.name,
        file.description,
        file.path,
        file.category,
        file.type,
      ];
      for (var i = 0; i < checks.length; i++) {
        if (checks[i] && checks[i].search(regex) > -1) return true;
      }
      return false;
    },
    uploaded(file) {
      this.fileStats = {
        file,
        size: file.size,
        origin: file.name,
        dateModified: file.lastModified,
        dateUploaded: Number(new Date()),
        type: file.type === 'application/zip' ? 'zip' : 'file',
      };
    },
    newFile() {
      this.$emit('input', {
        name: '(file without name)',
        description: '',
        origin: null,
        path: null,
        size: null,
        dateModified: null,
        dateUploaded: null,
        type: null,
        gridSize: null,
        category: null,
      });
    },
  },
  computed: {
    origin() {
      return this.fileStats.origin || this.value.origin;
    },
    dateUploaded() {
      const date = this.fileStats.dateUploaded || this.value.dateUploaded;
      return new Date(date).toLocaleDateString();
    },
    dateModified() {
      const date = this.fileStats.dateModified || this.value.dateModified;
      return new Date(date).toLocaleDateString();
    },
    type() {
      return this.fileStats.type || this.value.type;
    },
    size() {
      return this.fileStats.size || this.value.size;
    },
  },
  created() {
    window.db = this;
  },
};
