import gulp from 'gulp'
import browserSync from 'browser-sync'

import config from '../config'

export const bs = browserSync.create()

export function browserSyncTask () {
  bs.init(config.tasks.browserSync)

  gulp.watch(config.tasks.browserSync.watch, bs.reload)
}
