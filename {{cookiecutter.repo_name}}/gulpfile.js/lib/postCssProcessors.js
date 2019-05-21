module.exports = [
  require('postcss-easy-import'),
  require('postcss-sassy-mixins'),
  require('postcss-nested'),
  require('postcss-functions')({
    functions: {
      percentage: function (val1, val2) {
        let number = val1 / val2 * 100

        return number.toFixed(2) + '%'
      },
      columns: function (columns, totalColumns, gutter) {
        gutter = gutter ? `${gutter}px` : 'var(--Grid_Gutter)'

        return `calc((${columns} / ${totalColumns} * 100%) - (${gutter} * 2) * (${totalColumns} - ${columns}) / ${totalColumns})`
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
