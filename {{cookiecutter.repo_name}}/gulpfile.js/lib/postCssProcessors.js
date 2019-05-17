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
      },
      smooth_gradient: function (direction, startingColor, easingFunction, finalColor = 'transparent', stops = 5, colorMode = '') {
        // Code  adapted from the easing-gradients PostCSS plugin here:
        // https://github.com/larsenwork/postcss-easing-gradients

        const chroma = require('chroma-js')
        const easingCoordinates = require('easing-coordinates')

        // If the passed easing function isn't a real one, jump out here. See:
        // https://developer.mozilla.org/docs/Web/CSS/single-transition-timing-function
        const stepsFunction = 'steps'
        const cubicFunction = 'cubic-bezier'
        const easeShorthands = ['ease', 'ease-in', 'ease-out', 'ease-in-out']
        const timingFunctions = [...easeShorthands, cubicFunction, stepsFunction]
        if (!timingFunctions.includes(easingFunction.indexOf('(') !== -1 ? easingFunction.substring(0, easingFunction.indexOf('(')) : easingFunction)) {
          return ''
        }

        // Change 'transparent' into a transparent version of the starting color
        let colors = [startingColor, finalColor]
        colors = colors.map((color, i) => {
          return color === 'transparent' ? chroma(colors[Math.abs(i - 1)]).alpha(0).css('hsl') : color
        })

        // Get the stops for the gradient using the easing function.
        const coordinates = easingCoordinates.easingCoordinates(
          easingFunction,
          stops - 1
        )

        // Go through the coordinates and give them the colours for that stop.
        const colorStops = []
        const alphaDecimals = 2
        coordinates.forEach(coordinate => {
          const ammount = coordinate.y
          const percent = coordinate.x * 100
          let color = chroma.mix(colors[0], colors[1], ammount, colorMode).css('hsl')

          // Round the colours to the nearest 'alphaDecimals' decimal places
          const prefix = color.indexOf('(') !== -1 ? color.substring(0, color.indexOf('(')) : color
          const values = color.match(/\((.*)\)/).pop().split(',').map(string =>
            string.indexOf('%') === -1 ? +Number(string).toFixed(alphaDecimals) : string.trim()
          )

          // Pair the colour stop with the co-ords
          color = `${prefix}(${values.join(', ')})`

          // Add the new pair to the main output array. We don't need the stop % for the first and last items in the list.
          if (Number(coordinate.x) !== 0 && Number(coordinate.x) !== 1) {
            colorStops.push(`${color} ${+percent.toFixed(2)}%`)
          } else {
            colorStops.push(color)
          }
        })
        return `linear-gradient(${direction}, ${colorStops.join(', ')})`
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
