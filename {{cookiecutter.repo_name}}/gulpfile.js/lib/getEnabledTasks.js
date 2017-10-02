var config  = require('../config')

// Grouped by what can run in parallel
var assetTasks = ['fonts', 'iconFont', 'images', 'svgSprite']
var codeTasks = ['html', 'css', 'js']

module.exports = function(env) {
  var cssTasks = {
    watch: 'css',
    development: 'css',
    production: 'css:production'
  }

  function matchFilter(task) {
    if(config.tasks[task]) {
      if(task === 'js') {
        task = env === 'production' ? 'webpack:production' : false
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
    assetTasks: assetTasks.map(matchFilter).filter(exists),
    codeTasks: codeTasks.map(matchFilter).filter(exists)
  }
}
