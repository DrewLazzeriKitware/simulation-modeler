import DragAndDropFiles from '../DragAndDropFiles';

export default {
  name: 'FileDatabase',
  components: {
    DragAndDropFiles,
  },
  props: ['files', 'value'],
  data: () => ({ unsavedEdits: null, searchQuery: '' }),
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
      this.files[this.value] = Object.assign(
        this.files[this.value],
        this.unsavedEdits
      );
      if (window.PyWebVue) {
        // FIXME No Observer on files in Trame
        this.$forceUpdate();
      }
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
        dateCreated: null,
        dateUploaded: null,
        type: null,
        gridSize: null,
        category: null,
      });
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
  },
};
