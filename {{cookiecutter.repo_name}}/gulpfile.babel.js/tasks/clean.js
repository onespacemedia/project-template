import gulp from 'gulp'
import del from 'del'
import path from 'path'

import config from '../config'

export function cleanTask (cb) {
  const files = [path.join(config.root.dest, 'rev-manifest.json')]

  for (const key in config.tasks) {
    const task = config.tasks[key]
    if (task.dest) {
      const glob = '**/*' + (task.extensions ? ('.{' + task.extensions.join(',') + ',map}') : '')
      files.push(path.join(config.root.dest, task.dest, glob))
    }
  }

  // Don't touch node_modules or source files!
  files.push('!node_modules/**/*')
  files.push('!' + path.join(config.root.src, '/**/*'))

  del(files).then(function () {
    cb()
  })
}
