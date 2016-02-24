import browserSync from 'browser-sync'
import config from '../lib/webpack-multi-config'
import gulp from 'gulp'
import logger from '../lib/compileLogger'
import webpack from 'webpack'

export function webpackWatchTask (callback) {
  let initialCompile = false

  webpack(config('development')).watch(200, function (err, stats) {
    logger(err, stats)
    browserSync.reload()
    // On the initial compile, let gulp know the task is done
    if (!initialCompile) {
      initialCompile = true
      callback()
    }
  })
}

export function webpackProductionTask (callback) {
  webpack(config('production'), function (err, stats) {
    logger(err, stats)
    callback()
  })
}
