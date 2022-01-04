const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '../server/widgets/components/serve'),

  // runtimeCompiler: true,
  configureWebpack: {
    output: {
      libraryExport: 'default',
    },
  },

  transpileDependencies: ['vuetify'],
};
