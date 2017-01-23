var path = require('path')

module.exports = [
  require('postcss-import')({
    glob: true
  }),
  require('postcss-sassy-mixins'),
  require('postcss-conditionals'),
  require('postcss-apply'),
  require('postcss-nested'),
  require('postcss-functions')({
    glob: path.join(__dirname, '../../{{cookiecutter.package_name}}', 'assets', 'css', 'helpers', 'functions', '*.js')
  }),

  require('postcss-custom-properties'),
  require('postcss-custom-media'),
  require('postcss-media-minmax'),
  require('postcss-custom-selectors'),
  // Niceties
  require('postcss-assets')({
    basePath: '{{cookiecutter.package_name}}/assets/',
    loadPaths: ['img/'],
    baseUrl: '/static/'
  }),
  require('postcss-inline-svg')({
    path: '{{cookiecutter.package_name}}/assets/img/'
  }),
  require('postcss-brand-colors'),
  require('postcss-property-lookup'),
  require('postcss-lh')({
    rhythmUnit: 'vr'
  }),
  require('postcss-pxtorem'),
  require('postcss-will-change'),
  require('postcss-font-awesome'),
  require('postcss-round-subpixels'),
  require('postcss-calc'),
  require('postcss-hexrgba'),
  require('autoprefixer')({
    browsers: [
      'Android > 4.4.4',
      'Chrome > 40',
      'Edge > 12',
      'Explorer > 11',
      'Firefox > 35',
      'iOS > 8.4',
      'Opera > 30',
      'Safari > 9'
    ]
  }),
];
