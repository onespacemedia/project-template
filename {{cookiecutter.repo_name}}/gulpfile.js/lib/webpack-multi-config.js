var config = require('../config')
if(!config.tasks.js) return

var path            = require('path')
var pathToUrl       = require('./pathToUrl')
var webpack         = require('webpack')
var webpackManifest = require('./webpackManifest')
var BundleTracker   = require('webpack-bundle-tracker')
var ExtractText     = require('extract-text-webpack-plugin')

module.exports = function(env) {
  var jsSrc = path.resolve(config.root.src, config.tasks.js.src)
  var jsDest = path.resolve(config.root.dest, config.tasks.js.dest)
  var publicPath = pathToUrl('/static/build/', config.tasks.js.dest, '/')

  var filenamePattern = '[name]-[hash].js'

  var webpackConfig = {
    context: jsSrc,
    plugins: [
      new BundleTracker({filename: './webpack-stats.json'})
    ],
    resolve: {
      modules: [jsSrc, 'node_modules'],
      extensions: ['.js', '.vue', '.css', '.json'],
      alias: {
        'vue': 'vue/dist/vue'
      }
    },
    module: {
      noParse: /es6-promise\.js$/, // avoid webpack shimming process
      rules: [
        {
          enforce: 'pre',
          test: /\.vue$/,
          loader: 'eslint-loader',
          options: {
            formatter: require('eslint-friendly-formatter')
          },
          include: jsSrc,
          exclude: /(node_modules|bower_components|vendor)/
        },
        {
          enforce: 'pre',
          test: /\.js$/,
          loader: 'eslint-loader',
          options: {
            formatter: require('eslint-friendly-formatter')
          },
          include: jsSrc,
          exclude: /(node_modules|bower_components|vendor)/
        },
        {
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {
            postcss: require('../lib/postCssProcessors'),
            loaders: {
              js: 'babel-loader'
            }
          }
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          include: jsSrc,
          exclude: /node_modules/
        },
        {
          test: /\.json$/,
          loader: 'json-loader'
        }
      ]
    }
  }

  if(env === 'development') {
    webpackConfig.devtool = '#eval-source-map'

    // Create new entries object with webpack-hot-middleware added
    for (var key in config.tasks.js.entries) {
      var entry = config.tasks.js.entries[key]

      config.tasks.js.entries[key] = ['webpack-hot-middleware/client?&reload=true'].concat(entry)
    }

    webpackConfig.plugins.push(
      new webpack.DefinePlugin({
        'process.env': {
          'NODE_ENV': JSON.stringify('development')
        }
      }),
      new webpack.optimize.OccurrenceOrderPlugin(),
      new webpack.HotModuleReplacementPlugin(),
      new webpack.NoErrorsPlugin()
    )
  }

  if(env !== 'test') {
    // Karma doesn't need entry points or output settings
    webpackConfig.entry = config.tasks.js.entries

    webpackConfig.output= {
      path: path.normalize(jsDest),
      filename: filenamePattern,
      publicPath: publicPath
    }

    if(config.tasks.js.extractSharedJs) {
      // Factor out common dependencies into a vendor.js
      webpackConfig.plugins.push(
        new webpack.optimize.CommonsChunkPlugin({
          name: 'vendor',
          filename: filenamePattern,
        })
      )
    }
  }

  if(env === 'production') {
    webpackConfig.plugins.push(
      new ExtractText('[name][contenthash:8].css'),
      new webpack.DefinePlugin({
        'process.env': {
          'NODE_ENV': JSON.stringify('production')
        }
      }),
      new webpack.LoaderOptionsPlugin({
        minimize: true
      }),
      new webpack.optimize.UglifyJsPlugin({
        compress: {
          warnings: false
        },
        output: {
          comments: false
        }
      }),
      new webpack.optimize.OccurrenceOrderPlugin,
      new webpack.optimize.UglifyJsPlugin(),
      new webpack.NoErrorsPlugin()
    )

    webpackConfig.module.rules[2].options.loaders.css = ExtractText.extract({
      loader: 'css-loader',
      fallBackLoader: 'vue-style-loader'
    })
  }

  return webpackConfig
}
