var path = require('path')

module.exports = [
  require('postcss-import')({
    glob: true
  }),
  require('postcss-sassy-mixins'),
  require('postcss-conditionals'),
  require('postcss-nested'),
  require('postcss-simple-vars'),
  require('postcss-functions')({
    glob: path.join(__dirname, '../../{{cookiecutter.repo_name}}', 'assets', 'css', 'functions', '*.js')
  }),

  // Niceties
  require('postcss-assets')({
    basePath: 'streets/assets/',
    loadPaths: ['img/'],
    baseUrl: '/static/'
  }),
  require('postcss-brand-colors'),
  require('postcss-color-alpha'),
  require('postcss-property-lookup'),
  require('postcss-pxtorem'),
  require('postcss-will-change'),
  require('postcss-cssnext')({
    features: {
      autoprefixer: false,
      nesting: false,
      rem: false
    }
  }),
  require('postcss-round-subpixels'),
  require('autoprefixer')({
    browsers: ['> 1%', 'IE 9', 'IE 10', 'last 2 versions']
  }),
];
