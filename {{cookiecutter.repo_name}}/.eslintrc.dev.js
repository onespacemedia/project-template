const baseConfig = require('./.eslintrc')

const devConfig = baseConfig
devConfig.extends.push('prettier')
devConfig.rules['no-console'] = 0

module.exports = devConfig
