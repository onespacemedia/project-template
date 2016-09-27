var config  = require('../config')
var compact = require('lodash/compact')

// Grouped by what can run in parallel
var assetTasks = ['fonts', 'iconFont', 'images', 'svgSprite']
var codeTasks = ['html', 'css', 'js']

module.exports = function(env) {
  var jsTasks = {
    watch: 'webpack:watch',
    development: 'wepback:watch',
    production: 'webpack:production'
  }

  var cssTasks = {
    watch: 'css',
    development: 'css',
    production: 'css:production'
  }

  function matchFilter(task) {
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

  function exists(value) {
    return !!value
  }

  return {
    assetTasks: compact(assetTasks.map(matchFilter).filter(exists)),
    codeTasks: compact(codeTasks.map(matchFilter).filter(exists))
  }
}
