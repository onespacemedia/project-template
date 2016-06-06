var config       = require('../config')
if(!config.tasks.css) return

var gulp         = require('gulp')
var gulpif       = require('gulp-if')
var browserSync  = require('browser-sync')
var sourcemaps   = require('gulp-sourcemaps')
var postcss      = require('gulp-postcss')
var handleErrors = require('../lib/handleErrors')
var path         = require('path')
var reporter     = require('postcss-reporter')

var paths = {
  src: path.join(config.root.src, config.tasks.css.src, '/*.' + config.tasks.css.extensions),
  dest: path.join(config.root.dest, config.tasks.css.dest)
}

var cssTask = function () {
  return gulp.src(paths.src)
    .pipe(gulpif(!global.production, postcss([
      require('stylelint'),
      reporter({clearMessages: true})
    ])))
    .pipe(gulpif(!global.production, sourcemaps.init()))
    .pipe(postcss(require('../lib/postCssProcessors')))
    .on('error', console.log)
    .pipe(gulpif(!global.production, sourcemaps.write()))
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream())
}

gulp.task('css', cssTask)
module.exports = cssTask
