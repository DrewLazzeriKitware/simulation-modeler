import DragAndDropFiles from '../DragAndDropFiles';

export default {
  name: 'FileDatabase',
  components: {
    DragAndDropFiles,
  },
  props: ['files', 'currentFileIndex'],
  computed: {
    currentFile() {
      try {
        return this.files[this.currentFileIndex.index];
      } catch {
        return null;
      }
    },
  },
  methods: {
    iconFromType(type) {
      if (type === 'zip') return 'mdi-folder-zip';
      if (type === 'folder') return 'mdi-folder';
      return 'mdi-file';
    },
  },
};
