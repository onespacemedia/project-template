var path = require('path')

module.exports = [
  require('postcss-import')({
    glob: true
  }),
  require('postcss-cssnext')({
    features: {
      autoprefixer: false,
      nesting: false,
      rem: false
    }
  }),
  require('rucksack-css')({
    autoprefixer: false
  }),
  require('postcss-sassy-mixins'),
  require('postcss-conditionals'),
  require('postcss-nested'),
  require('postcss-functions')({
    glob: path.join(__dirname, '../../{{cookiecutter.package_name}}', 'assets', 'css', 'functions', '*.js')
  }),

  // Niceties
  require('postcss-assets')({
    basePath: '{{cookiecutter.package_name}}/assets/',
    loadPaths: ['img/'],
    baseUrl: '/static/'
  }),
  require('postcss-brand-colors'),
  require('postcss-property-lookup'),
  require('postcss-pxtorem'),
  require('postcss-will-change'),
  require('postcss-font-awesome'),
  require('postcss-round-subpixels'),
  require('autoprefixer')({
    browsers: ['ie 11', 'last 2 versions']
  }),
];
