export default {
  SimulationType: {
    shortcuts: {
      wells: false,
      climate: true,
      contaminants: false,
      saturated: 'Variably Saturated',
    },
  },
  NavigationDropDown: {
    views: [
      'File Database',
      'Simulation Type',
      'Domain',
      'Boundary Conditions',
      'Subsurface Properties',
      'Wells',
      'CLM',
      'Solver',
      'Project Generator',
    ],
    currentView: {
      view: 'Simulation Type',
    },
  },
  FileDatabaseErrors: {
    errors: ['Problem 01'],
    workingDirectory: '/opt/fake/directory',
    fileDB: '/home/fake/project',
  },
};
