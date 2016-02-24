import browserSync from 'browser-sync'
import changed from 'gulp-changed'
import gulp from 'gulp'
import path from 'path'

import config from '../config'

const paths = {
  src: [path.join(config.root.src, config.tasks.images.src, '/**'), path.join(config.root.appSrc, config.tasks.images.src, '/**')],
  dest: path.join(config.root.dest, config.tasks.images.dest)
}

export function imagesTask () {
  return gulp.src(paths.src)
    .pipe(changed(paths.dest)) // Ignore unchanged files
    .pipe(gulp.dest(paths.dest))
    .pipe(browserSync.stream())
}
