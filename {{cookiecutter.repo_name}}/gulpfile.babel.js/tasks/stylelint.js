import browserSync from 'browser-sync'
import gulp from 'gulp'
import path from 'path'
import postcss from 'gulp-postcss'
import reporter from 'postcss-reporter'

import config from '../config'

const paths = {
  src: path.join(config.root.src, config.tasks.css.src, '/**/*.' + config.tasks.css.extensions),
  dest: path.join(config.root.dest, config.tasks.css.dest)
}

export function styleLintTask () {
  const processors = [
    require('stylelint'),
    reporter({ clearMessages: true })
  ]

  return gulp.src(paths.src)
    .pipe(postcss(processors))
}
