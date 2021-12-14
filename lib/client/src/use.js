import NavigationDropDown from './components/NavigationDropDown';
import SimputStandin from './components/SimputStandin';
import SimulationType from './components/SimulationType';
import OverlayDatabaseErrors from './components/OverlayDatabaseErrors';
import FileDatabase from './components/FileDatabase';
import Domain from './components/Domain';
import BoundaryConditions from './components/BoundaryConditions';
import SubSurface from './components/SubSurface';
import Solver from './components/Solver';
import ProjectGeneration from './components/ProjectGeneration';

import SimputDomain from './components/SimputDomain';
import SimputSolver from './components/SimputSolver';

const components = {
  NavigationDropDown,
  SimulationType,
  SimputStandin,
  OverlayDatabaseErrors,
  FileDatabase,
  Domain,
  BoundaryConditions,
  SubSurface,
  Solver,
  ProjectGeneration,

  // Simput components
  SimputSolver,
  SimputDomain,
};

export default {
  install(Vue) {
    Object.keys(components).forEach((name) => {
      Vue.component(name, components[name]);
    });
  },
};
