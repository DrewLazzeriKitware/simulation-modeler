const path = require("path");

module.exports = {
  outputDir: path.resolve(__dirname, "../python/src/pfweb/dist"),
  // runtimeCompiler: true,
  configureWebpack: {
    output: {
      libraryExport: "default"
    }
  },
  chainWebpack: config => {
    // For library usage
    config.externals({ vue: "Vue", Vue: "Vue" });
  }
};
