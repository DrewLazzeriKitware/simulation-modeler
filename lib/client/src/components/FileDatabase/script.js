import DragAndDropFiles from '../DragAndDropFiles';

export default {
  name: 'FileDatabase',
  components: {
    DragAndDropFiles,
  },
  props: ['files', 'value', 'db-update'],
  data() {
    return {
      searchQuery: '',
      fileStats: {},
      file: null,
      formContent: this.value,
    };
  },
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
        size: file.size,
        origin: file.name,
        dateModified: file.lastModified,
        dateUploaded: Number(new Date()),
        type: file.type === 'application/zip' ? 'zip' : 'file',
      };
      this.file = file;
    },
    selectFile(id) {
      this.trigger(this.dbUpdate, ['selectFile', id]);
    },
    removeFile(id) {
      this.trigger(this.dbUpdate, ['removeFile', id]);
    },
    downloadSelectedFile() {
      this.trigger(this.dbUpdate, ['downloadSelectedFile']);
    },
    resetSelectedFile() {
      this.trigger(this.dbUpdate, ['resetSelectedFile']);
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
    save() {
      if (this.file) {
        this.set('dbFileExchange', this.file);
      }
      this.$emit('input', { ...this.formContent, ...this.fileStats });
    },
  },
  computed: {
    origin() {
      return this.fileStats.origin || this.formContent.origin;
    },
    dateUploaded() {
      const date = this.fileStats.dateUploaded || this.formContent.dateUploaded;
      if (!date) return date;
      return new Date(date).toLocaleDateString();
    },
    dateModified() {
      const date = this.fileStats.dateModified || this.formContent.dateModified;
      if (!date) return date;
      return new Date(date).toLocaleDateString();
    },
    type() {
      return this.fileStats.type || this.formContent.type;
    },
    size() {
      return this.fileStats.size || this.formContent.size;
    },
    selectedFileIndex() {
      return Object.values(this.files).findIndex(
        (file) => file.id === this.formContent.id
      );
    },
  },
  watch: {
    value() {
      this.formContent = { ...this.value };
    },
  },
  created() {
    window.db = this;
  },
  inject: ['set', 'trigger'],
};
