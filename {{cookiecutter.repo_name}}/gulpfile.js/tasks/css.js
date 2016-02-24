var config       = require('../config')
if(!config.tasks.css) return

var gulp         = require('gulp')
var browserSync  = require('browser-sync')
var sourcemaps   = require('gulp-sourcemaps')
var postcss      = require('gulp-postcss')
var handleErrors = require('../lib/handleErrors')
var path         = require('path')

var paths = {
  src: path.join(config.root.src, config.tasks.css.src, '/*.' + config.tasks.css.extensions),
  dest: path.join(config.root.dest, config.tasks.css.dest)
}

var cssTask = function () {
  return gulp.src(paths.src)
    .pipe(sourcemaps.init())
    .pipe(postcss(require('../lib/postCssProcessors')))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream({match: '**/*.css'}))
}

var cssProductionTask = function () {
  return gulp.src(path.join(config.root.dest, config.tasks.css.dest, '/*.' + config.tasks.css.extensions))
    .pipe(postcss([require('cssnano')({
      mergeRules: false
    })]))
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream({match: '**/*.css'}))
}

gulp.task('css', ['stylelint'], cssTask)
gulp.task('css:production', ['css', 'stylelint'], cssProductionTask)
module.exports = cssTask
