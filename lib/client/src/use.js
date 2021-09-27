import HelloWorld from './components/HelloWorld.vue';
import NavigationDropDown from './components/NavigationDropDown';

const components = { HelloWorld, NavigationDropDown };

export default {
  install(Vue) {
    Object.keys(components).forEach((name) => {
      Vue.component(name, components[name]);
    });
  },
};
