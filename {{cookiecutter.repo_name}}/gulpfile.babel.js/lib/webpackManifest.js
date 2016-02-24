import fs from 'fs'
import path from 'path'

export default function(publicPath, dest, filename) {
  filename = filename || 'rev-manifest.json'

  return function() {
    this.plugin("done", function(stats) {
      stats = stats.toJson()
      const chunks = stats.assetsByChunkName
      const manifest = {}

      for (const key in chunks) {
        const originalFilename = key + '.js'
        manifest[path.join(publicPath, originalFilename)] = path.join(publicPath, chunks[key][0])
      }

      fs.writeFileSync(
        path.join(process.cwd(), dest, filename),

        JSON.stringify(manifest)
      )
    })
  }
}
