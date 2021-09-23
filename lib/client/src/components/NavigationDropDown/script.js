export default {
  name: "NavigationDropDown",
  props: ['currentView', 'views'],
  data: () => ({}),
  computed: {
    canMoveForward() {
      const i = this.views.indexOf(this.currentView.view);
      return i !== -1 && i < this.views.length - 1
    },
    canMoveBackward() {
      const i = this.views.indexOf(this.currentView.view);
      return i !== -1 && i > 0;
    }
  },
  methods: {
    moveBackward() {
      const i = this.views.indexOf(this.currentView.view);
      this.currentView.view = this.views[i - 1];
    },
    moveForward() {
      const i = this.views.indexOf(this.currentView.view);
      this.currentView.view = this.views[i + 1];
    }


  }

};
