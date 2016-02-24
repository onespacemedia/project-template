import gulp from 'gulp'
import browserSync from 'browser-sync'

import config from '../config'

export function browserSyncTask () {
  browserSync.init(config.tasks.browserSync)

  gulp.watch(config.tasks.browserSync.watch, browserSync.reload)
}
