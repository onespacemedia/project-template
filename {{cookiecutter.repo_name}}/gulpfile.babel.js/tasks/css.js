import gulp from 'gulp'
import browserSync from 'browser-sync'
import sourcemaps from 'gulp-sourcemaps'
import postcss from 'gulp-postcss'
import path from 'path'

import handleErrors from '../lib/handleErrors'
import postCssProcessors from '../lib/postCssProcessors'

import config from '../config'

const paths = {
  src: path.join(config.root.src, config.tasks.css.src, '/*.' + config.tasks.css.extensions),
  dest: path.join(config.root.dest, config.tasks.css.dest)
}

export function cssTask () {
  return gulp.src(paths.src)
    .pipe(sourcemaps.init())
    .pipe(postcss(postCssProcessors))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream({ match: '**/*.css' }))
}

export function cssWatch () {
  gulp.watch(path.join(config.root.src, config.tasks.css.src, '**/*.' + config.tasks.css.extensions), gulp.series('css'))
}

export function cssProductionTask () {
  return gulp.src(path.join(config.root.dest, config.tasks.css.dest, '/*.' + config.tasks.css.extensions))
    .pipe(postcss([require('cssnano')({
      mergeRules: false
    })]))
    .pipe(gulp.dest(paths.dest))
}
