import DragAndDropFiles from '../DragAndDropFiles';

export default {
  name: 'FileDatabase',
  components: {
    DragAndDropFiles,
  },
  props: ['files', 'value'],
  data: () => ({ unsavedEdits: null, searchQuery: '', isNewFile: false }),
  computed: {
    currentFile() {
      if (!this.unsavedEdits) this.resetEdits();
      return this.unsavedEdits;
    },
  },
  watch: {
    value() {
      this.resetEdits();
    },
  },
  methods: {
    iconFromType(type) {
      if (type === 'zip') return 'mdi-folder-zip';
      if (type === 'folder') return 'mdi-folder';
      return 'mdi-file';
    },
    save() {
      const newFile = {
        ...this.files[this.value],
        ...this.unsavedEdits,
      };
      this.isNewFile = false;
      this.$emit('updateFiles', { newFile, index: this.value });
    },
    resetEdits() {
      this.unsavedEdits = Object.assign({}, this.files[this.value]);
    },
    newFile() {
      this.files.push({
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
      this.isNewFile = true;
      this.$emit('input', this.files.length - 1);
      this.resetEdits();
    },
    remove(index) {
      this.files.splice(index, 1);
      if (index === this.value) {
        this.$emit('input', 0);
      }
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
      this.unsavedEdits.file = file;
      this.unsavedEdits.size = file.size;
      this.unsavedEdits.origin = file.name;
      this.unsavedEdits.dateModified = file.lastModified;
      this.unsavedEdits.dateUploaded = Number(new Date());
      if (file.type === 'application/zip') {
        this.unsavedEdits.type = 'zip';
      } else {
        this.unsavedEdits.type = 'file';
      }
    },
  },
  created() {
    window.db = this;
  },
};
