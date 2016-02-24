const config = require('./config')

import gulp from 'gulp'

import {browserSyncTask} from './tasks/browserSync'
import {cleanTask} from './tasks/clean'
import {cssTask, cssWatch, cssProductionTask} from './tasks/css'
import {fontsTask} from './tasks/fonts'
import {imagesTask} from './tasks/images'
import {styleLintTask} from './tasks/stylelint'
import {webpackWatchTask, webpackProductionTask} from './tasks/webpack'

gulp.task('clean', cleanTask)

gulp.task('css', gulp.series(
  styleLintTask,
  cssTask
))
gulp.task('css:watch', cssWatch)
gulp.task('css:production', cssProductionTask)

gulp.task('fonts', fontsTask)
gulp.task('images', imagesTask)

gulp.task('browserSync', browserSyncTask)

gulp.task('webpack:watch', webpackWatchTask)
gulp.task('webpack:production', webpackProductionTask)

gulp.task('production',
  gulp.series(
    'css',
    gulp.parallel(
      'css:production', 'images', 'webpack:production'
    )
  )
)

gulp.task('default',
  gulp.series(
    'clean',
    gulp.parallel('css', 'fonts', 'images'),
    gulp.parallel('css:watch', 'webpack:watch', 'browserSync')
  )
)
