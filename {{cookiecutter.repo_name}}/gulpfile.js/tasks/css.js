var config = require('../config')
if (!config.tasks.css) return

var gulp = require('gulp')
var browserSync = require('browser-sync')
var sourcemaps = require('gulp-sourcemaps')
var postcss = require('gulp-postcss')
var handleErrors = require('../lib/handleErrors')
var path = require('path')
var stylelint = require('gulp-stylelint')
var reporter = require('postcss-reporter')

var paths = {
  src: path.join(config.root.src, config.tasks.css.src, '/*.' + config.tasks.css.extensions),
  dest: path.join(config.root.dest, config.tasks.css.dest)
}

var cssTask = function () {
  return gulp.src(paths.src)
      .pipe(stylelint({
        reporters: [
          { formatter: 'string', console: true }
        ],
        configFile: './stylelint.config.js',
        failAfterError: false
      }))
      .pipe(sourcemaps.init())
      .pipe(postcss(require('../lib/postCssProcessors')))
      .on('error', console.log)
      .pipe(sourcemaps.write())
      .pipe(gulp.dest(paths.dest))
      .pipe(browserSync.stream({ match: '**/*.css' }))
}

var cssProductionTask = function () {
  return gulp.src(path.join(config.root.dest, config.tasks.css.dest, '/*.' + config.tasks.css.extensions))
      .pipe(postcss([require('cssnano')({
        mergeRules: false
      })]))
      .pipe(gulp.dest(paths.dest))
      .pipe(browserSync.stream({ match: '**/*.css' }))
}

gulp.task('css', cssTask)
gulp.task('css:production', ['css'], cssProductionTask)
module.exports = cssTask
