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
  src: path.join(config.root.src, config.tasks.css.src, '/*.{' + config.tasks.css.extensions + '}'),
  dest: path.join(config.root.dest, config.tasks.css.dest)
}

var cssTask = function () {
  return gulp.src(paths.src)
    .pipe(sourcemaps.init())
    .pipe(postcss([
      // Sassy based plugins
      require('postcss-partial-import'),
      require('postcss-sassy-mixins'),
      require('postcss-advanced-variables'),
      require('postcss-custom-selectors'),
      require('postcss-custom-media'),
      require('postcss-custom-properties'),
      require('postcss-media-minmax'),
      require('postcss-color-function'),
      require('postcss-nested'),
      require('postcss-atroot'),
      require('postcss-property-lookup'),
      require('postcss-extend'),
      require('postcss-selector-matches'),
      require('postcss-selector-not'),

      // Niceties
      require('postcss-assets')({
        basePath: '{{cookiecutter.package_name}}/assets/',
        loadPaths: ['img/'],
        baseUrl: '/static/'
      }),
      require('postcss-brand-colors'),
      require('postcss-fakeid'),
      require('postcss-flexbugs-fixes'),
      require('postcss-property-lookup'),
      require('postcss-pxtorem'),
      require('postcss-quantity-queries'),
      require('postcss-will-change'),
      require('autoprefixer'),
    ]))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream({match: '**/*.css'}))
}

gulp.task('css', ['stylelint'], cssTask)
module.exports = cssTask
