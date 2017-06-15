const baseConfig = require('./.eslintrc')

const devConfig = baseConfig
devConfig.extends.push('prettier')

module.exports = devConfig
