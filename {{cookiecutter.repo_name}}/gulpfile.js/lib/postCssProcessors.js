module.exports = [
  require('postcss-easy-import'),
  require('postcss-sassy-mixins'),
  require('postcss-conditionals'),
  require('postcss-nested'),
  require('postcss-functions')({
    functions: {
      percentage: function (val1, val2) {
        let number = val1 / val2 * 100

        return number.toFixed(2) + '%'
      },
      columns: function (n, t, gutter) {
        gutter = gutter ? `${gutter}px` : 'var(--Grid_Gutter)'

        return `calc((${n} / ${t} * 100%) - (${gutter} * 2) * (${t} - ${n}) / ${t})`
      }
    }
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
  require('postcss-round-subpixels'),
  require('postcss-hexrgba'),
  require('autoprefixer'),
];
