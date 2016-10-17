var config = require('../config')
var gulp   = require('gulp')
var path   = require('path')
var watch  = require('gulp-watch')

var watchTask = function() {
  var watchableTasks = ['fonts', 'images', 'html', 'css']

  watchableTasks.forEach(function(taskName) {
    var task = config.tasks[taskName]
    if(task) {
      var glob = path.join(config.root.src, task.src, '**/*.{' + task.extensions.join(',') + '}')

      if (task.src === 'css') {
        glob = '{' + path.join(config.root.src, task.src, '**/*.{' + task.extensions.join(',') + '}') + ',' + path.join(config.root.src + '/js/**/*.css') + ',' + path.join(config.root.appSrc + '/**/*.css}')
      }

      watch(glob, function() {
       require('./' + taskName)()
      })
    }
  })
}

gulp.task('watch', ['browserSync'], watchTask)
module.exports = watchTask
