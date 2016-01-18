var path = require('path')

module.exports = [
  require('postcss-import')({
    glob: true
  }),
  require('postcss-mixins'),
  require('postcss-functions')({
    glob: path.join(__dirname, '../../example_project', 'assets', 'css', 'functions', '*.js')
  }),

  // Niceties
  require('postcss-brand-colors'),
  require('postcss-property-lookup'),
  require('postcss-pxtorem'),
  require('postcss-will-change'),
  require('postcss-cssnext')({
    features: {
      rem: false
    }
  }),
  require('autoprefixer')({
    browsers: ['> 1%', 'IE 9', 'IE 10', 'last 2 versions']
  }),
];
