var config       = require('../config')
if(!config.tasks.css) return

var gulp         = require('gulp')
var browserSync  = require('browser-sync')
var sass         = require('gulp-sass')
var sourcemaps   = require('gulp-sourcemaps')
var postcss      = require('gulp-postcss')
var handleErrors = require('../lib/handleErrors')
var autoprefixer = require('gulp-autoprefixer')
var path         = require('path')

var paths = {
  src: path.join(config.root.src, config.tasks.css.src, '/**/*.{' + config.tasks.css.extensions + '}'),
  dest: path.join(config.root.dest, config.tasks.css.dest)
}

var cssTask = function () {
  return gulp.src(paths.src)
    .pipe(sourcemaps.init())
    .pipe(sass(config.tasks.css.sass))
    .on('error', handleErrors)
    .pipe(postcss([
      require('postcss-assets')({
        basePath: 'csap/assets/',
        loadPaths: ['img/'],
        baseUrl: '/static/site/build/'
      }),
      require('postcss-at2x'),
      require('autoprefixer'),
      require('postcss-brand-colors'),
      require('postcss-fakeid'),
      require('postcss-flexbugs-fixes'),
      require('postcss-property-lookup'),
      require('postcss-pxtorem'),
      require('postcss-quantity-queries'),
      require('postcss-will-change')
    ]))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream({match: '**/*.css'}))
}

gulp.task('css', ['stylelint'], cssTask)
module.exports = cssTask
