import config from '../config'

import path from 'path'
import webpack from 'webpack'
import webpackManifest from './webpackManifest'
import BundleTracker from 'webpack-bundle-tracker'

export default function (env) {
  const jsSrc = path.resolve(config.root.src, config.tasks.js.src)
  const jsDest = path.resolve(config.root.dest, config.tasks.js.dest)
  const publicPath = path.join('/static/build/', config.tasks.js.dest, '/')
  const filenamePattern = '[name].js'
  const extensions = config.tasks.js.extensions.map((extension) => {
    return '.' + extension
  })

  const webpackConfig = {
    context: jsSrc,
    plugins: [
      new BundleTracker({ filename: './webpack-stats.json' })
    ],
    resolve: {
      root: jsSrc,
      extensions: [''].concat(extensions)
    },
    module: {
      preLoaders: [
        {
          test: /\.js$/,
          loader: 'eslint',
          exclude: /(node_modules|bower_components)/
        }
      ],
      loaders: [
        {
          test: /\.js$/,
          loader: 'babel-loader',
          exclude: /node_modules/
        },
        {
          test: /\.vue$/,
          loader: 'vue'
        }
      ]
    },
    vue: {
      loaders: {
        js: 'babel'
      }
    },
    babel: {
      presets: ['es2015', 'stage-0'],
      plugins: ['transform-runtime']
    }
  }

  if (env !== 'test') {
    // Karma doesn't need entry points or output settings
    webpackConfig.entry = config.tasks.js.entries

    webpackConfig.output = {
      path: path.normalize(jsDest),
      filename: filenamePattern,
      publicPath: publicPath
    }

    if (config.tasks.js.extractSharedJs) {
      // Factor out common dependencies into a shared.js
      webpackConfig.plugins.push(
        new webpack.optimize.CommonsChunkPlugin({
          name: 'shared',
          filename: filenamePattern,
        })
      )
    }
  }

  if (env === 'development') {
    webpackConfig.devtool = 'source-map'
    webpack.debug = true
  }

  if (env === 'production') {
    webpackConfig.plugins.push(
      new webpackManifest(publicPath, config.root.dest),
      new webpack.DefinePlugin({
        'process.env': {
          'NODE_ENV': JSON.stringify('production')
        }
      }),
      new webpack.optimize.DedupePlugin(),
      new webpack.NoErrorsPlugin()
    )
  }

  return webpackConfig
}
