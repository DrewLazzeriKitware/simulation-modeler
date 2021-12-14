const path = require("path");

module.exports = {
  outputDir: path.resolve(__dirname, "../server/widgets/widgets/serve"),

  // runtimeCompiler: true,
  configureWebpack: {
    output: {
      libraryExport: "default"
    }
  },

  transpileDependencies: [
    'vuetify'
  ]
};
