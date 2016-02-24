var config = require('../config')
var compact = require('lodash/array/compact')

// Grouped by what can run in parallel
var assetTasks = ['fonts', 'images']
var codeTasks = ['css', 'js']

module.exports = function(env) {
  var jsTasks = {
    watch: 'webpack:watch',
    development: 'webpack:watch',
    production: 'webpack:production'
  }

  var cssTasks = {
    watch: 'css',
    development: 'css',
    production: 'css:production'
  }

  var matchFilter = function(task) {
    if(config.tasks[task]) {
      if(task === 'js') {
        task = jsTasks[env] || jsTasks.watch
      }

      if(task === 'css') {
        task = cssTasks[env] || cssTasks.watch
      }

      return task
    }
  }

  return {
    assetTasks: compact(assetTasks.map(matchFilter)),
    codeTasks: compact(codeTasks.map(matchFilter))
  }
}
