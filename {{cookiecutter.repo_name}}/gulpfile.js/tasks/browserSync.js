var browserSync = require('browser-sync')
var config      = require('../config')
var gulp        = require('gulp')

var browserSyncTask = function() {
  browserSync.init(config.tasks.browserSync)

  gulp.watch([
    '{{cookiecutter.package_name}}/apps/**/templates/**/*.html',
    '{{cookiecutter.package_name}}/templates/**/*.html'
  ], browserSync.reload)
}
gulp.task('browserSync', browserSyncTask)
module.exports = browserSyncTask
