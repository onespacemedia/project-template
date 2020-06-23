const path = require('path');
const loaders = require('./loaders');
const plugins = require('./plugins');

const ASSET_PATH = process.env.ASSET_PATH || '/static/build/';

const config = {
  entry: {
    main: path.resolve(__dirname, '../{{cookiecutter.package_name}}/assets/js/main.js'),
    staff: path.resolve(__dirname, '../{{cookiecutter.package_name}}/assets/js/staff.js'),
    wysiwyg: path.resolve(__dirname, '../{{cookiecutter.package_name}}/assets/js/wysiwyg.js'),
    iefallback: path.resolve(__dirname, '../alchemie_technology/assets/js/ie-fallback.js')
  },
  module: {
    rules: [
      loaders.CSSLoader,
      loaders.JSLoader,
      loaders.ESLintLoader,
      loaders.VueLoader,
      loaders.FileLoader,
      loaders.FontLoader,
    ]
  },
  output: {
    path: path.resolve(__dirname, '../{{cookiecutter.package_name}}/static/build'),
    filename: 'js/[name]-[hash].bundle.js',
    publicPath: ASSET_PATH,
  },
  plugins: [
    plugins.StyleLintPlugin,
    plugins.MiniCssExtractPlugin,
    plugins.VueLoaderPlugin,
    plugins.BundleTrackerPlugin,
  ],
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.js' // Use the full build the includes the runtime Complier (adds ~10kb)
    }
  },
  watchOptions: {
    aggregateTimeout: 300,
    ignored: /node_modules/,
    poll: 500,
  },
  devServer: {
    overlay: true,
    port: 3000,
    proxy: [{
      context: () => true,
      target: 'http://0.0.0.0:8000/'
    }],
    contentBase: [
      './{{cookiecutter.package_name}}/**/*.html'
    ],
  }
};

module.exports = (env, argv) => {
  config.mode = argv.mode || 'development'

  if (config.mode === 'development') {
    config.plugins.push(plugins.BundleAnalyzerPlugin)
    config.plugins.push(plugins.SourceMapsPlugin)
    config.devtool = false
  }

  return config
}
