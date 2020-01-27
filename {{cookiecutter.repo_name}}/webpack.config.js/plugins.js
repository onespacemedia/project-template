const path = require('path');
const _MiniCssExtractPlugin = require('mini-css-extract-plugin');
const _StyleLintPlugin = require('stylelint-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader')
const BundleTracker = require('webpack-bundle-tracker');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const SourceMapDevToolPlugin = require('webpack').SourceMapDevToolPlugin;

const MiniCssExtractPlugin = new _MiniCssExtractPlugin({
  filename: 'css/[name]-[hash].bundle.css',
  chunkFilename: '[id].css',
  hmr: process.env.NODE_ENV === 'development',
});

const StyleLintPlugin = new _StyleLintPlugin({
  configFile: path.resolve(__dirname, '../stylelint.config.js'),
  context: path.resolve(__dirname, '../{{cookiecutter.package_name}}/assets/css'),
  files: '**/*.css',
  failOnError: false,
  quiet: false,
});

const SourceMapsPlugin = new SourceMapDevToolPlugin({
  filename: '[file].map'
})

module.exports = {
  MiniCssExtractPlugin,
  StyleLintPlugin,
  VueLoaderPlugin: new VueLoaderPlugin,
  BundleTrackerPlugin: new BundleTracker({filename: './webpack-stats.json'}),
  BundleAnalyzerPlugin: new BundleAnalyzerPlugin({openAnalyzer: false}),
  SourceMapsPlugin
};
