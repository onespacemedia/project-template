import browserSync from 'browser-sync'
import changed from 'gulp-changed'
import gulp from 'gulp'
import path from 'path'

import config from '../config'

const paths = {
  src: path.join(config.root.src, config.tasks.fonts.src, '/**/*'),
  dest: path.join(config.root.dest, config.tasks.fonts.dest)
}

export function fontsTask () {
  return gulp.src(paths.src, { since: gulp.lastRun('fonts') })
    .pipe(changed(paths.dest)) // Ignore unchanged files
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream())
}
