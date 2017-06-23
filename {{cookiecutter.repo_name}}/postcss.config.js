const path = require('path')

module.exports = {
  plugins: {
    'postcss-easy-import': {},
    'postcss-sassy-mixins': {},
    'postcss-conditionals': {},
    'postcss-apply': {},
    'postcss-nested': {},
    'postcss-functions': {
      glob: path.join(__dirname, '../../cms_test', 'assets', 'css', 'helpers', 'functions', '*.js')
    },
    'postcss-custom-properties': {},
    'postcss-custom-media': {},
    'postcss-media-minmax': {},
    'postcss-custom-selectors': {},
    'postcss-assets': {
      basePath: 'cms_test/assets/',
      loadPaths: ['img/'],
      baseUrl: '/static/'
    },
    'postcss-inline-svg': {
      path: 'cms_test/assets/img/'
    },
    'postcss-brand-colors': {},
    'postcss-property-lookup': {},
    'postcss-lh': {
      rhythmUnit: 'vr'
    },
    'postcss-pxtorem': {},
    'postcss-will-change': {},
    'postcss-font-awesome': {},
    'postcss-round-subpixels': {},
    'postcss-calc': {},
    'postcss-hexrgba': {},
    'autoprefixer': {}
  }
}
