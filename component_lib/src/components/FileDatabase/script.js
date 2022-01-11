import DragAndDropFiles from '../DragAndDropFiles';


export default {
  name: 'FileDatabase',
  components: {
    DragAndDropFiles,
  },
  props: ['files', 'fileCategories', 'value', 'db-update'],
  data() {
    return {
      searchQuery: '',
      fileStats: {},
      file: null,
      formContent: this.value || {},
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
      const checks = [file.name, file.description, file.category, file.type];
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
      this.cancel();
    },
    newFile() {
      this.fileStats = {};
      let name = 'unnamed file';
      let count = 1;
      const fileList = Object.values(this.files);
      while (fileList.find((file) => file.name === name + ' ' + count)) {
        count++;
      }
      name = name + ' ' + count;
      this.$emit('input', {
        name,
        description: '',
        origin: null,
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
    cancel() {
      this.formContent = { ...(this.value || {}) };
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
    hasFiles() {
      return Object.keys(this.files).length > 0;
    }
  },
  watch: {
    value() {
      this.cancel();
    },
  },
  inject: ['set', 'trigger'],
};
