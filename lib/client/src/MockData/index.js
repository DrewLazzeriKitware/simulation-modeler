export default {
  // Views
  FileDatabase: {
    files: [
      {
        name: 'MyIndicator',
        description:
          'This is my indicator. I made it. There are many like it, but this one is mine.',
        origin: '/oldDrive/oldFolder/originalProject',
        path: '/opt/fileDatabases/filedb1',
        size: 672716,
        dateCreated: daysAgo(100),
        dateUploaded: daysAgo(50),
        type: 'file',
        gridSize: [50, 50, 2],
        category: 'Indicator',
      },
      {
        name: 'Rain Forcing',
        description:
          'This simulates heavy rain across the entire surface. It was made by...',
        origin: '/oldDrive/oldFolder/otherProject',
        path: '/opt/fileDatabases/filedb1',
        size: 5321298,
        dateCreated: daysAgo(93),
        dateUploaded: daysAgo(50),
        type: 'zip',
        gridSize: null,
        category: 'CLM',
      },
    ],
  },
  SimulationType: {
    shortcuts: {
      wells: false,
      climate: true,
      contaminants: false,
      saturated: 'Variably Saturated',
    },
  },
  // Helpers
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
      view: 'File Database',
    },
  },
  OverlayDatabaseErrors: {
    errors: ['Problem 01'],
    workingDirectory: '/opt/fake/directory',
    fileDB: '/home/fake/project',
  },
};

function daysAgo(days) {
  var now = new Date();
  var oneDayInMilliseconds = 1000 * 60 * 60 * 24 * 2;
  return new Date(now - days * oneDayInMilliseconds);
}
