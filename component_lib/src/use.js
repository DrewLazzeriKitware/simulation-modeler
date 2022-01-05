import NavigationDropDown from './components/NavigationDropDown';
import SimputStandin from './components/SimputStandin';
import SimulationType from './components/SimulationType';
import FileDatabase from './components/FileDatabase';
import Solver from './components/Solver';

import SimputSolver from './components/SimputSolver';

const components = {
  NavigationDropDown,
  SimulationType,
  SimputStandin,
  FileDatabase,
  Solver,

  // Simput components
  SimputSolver,
};

export default {
  install(Vue) {
    Object.keys(components).forEach((name) => {
      Vue.component(name, components[name]);
    });
  },
};
