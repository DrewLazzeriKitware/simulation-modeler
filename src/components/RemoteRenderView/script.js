import vtkRemoteView from 'vtk.js/Sources/Rendering/Misc/RemoteView';

export default {
  name: 'RemoteRenderView',
  props: {
    viewId: { type: String, required: true },
    client: { type: Object, default: null },
  },
  created() {
    this.view = vtkRemoteView.newInstance({
      rpcWheelEvent: 'viewport.mouse.zoom.wheel',
    });
    this.view.setInteractiveRatio(1);
  },
  mounted() {
    this.view.setContainer(this.$el.querySelector('.js-renderer'));
    const session = this.client.getConnection().getSession();
    this.view.setSession(session);
    this.view.setViewId(this.viewId);
    this.view.render();
    this.view.resize();
  },
  methods: {
    onResize() {
      if (this.view) this.view.resize();
    },
    mouseDown() {
      this.$el.querySelector('.js-renderer').focus();
    },
  },
};
