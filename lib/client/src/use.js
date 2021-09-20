import HelloWorld from "./components/HelloWorld.vue";

const components = { HelloWorld };

export default {
  install(Vue) {
    Object.keys(components).forEach(name => {
      Vue.component(name, components[name]);
    });
  }
};
