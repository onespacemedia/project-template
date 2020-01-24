module.exports = {
  plugins: {
    'postcss-import-ext-glob': {},
    'postcss-import': {},
    'postcss-easy-import': {},
    'postcss-sassy-mixins': {},
    'postcss-lh': {
      unit: 'vr'
    },
    'postcss-nested': {},
    'postcss-functions': {
      functions: {
        percentage (val1, val2) {
          const number = val1 / val2 * 100

          return `${number.toFixed(2)}%`
        },
        columns (columns, totalColumns, gutter) {
          gutter = gutter ? `${gutter}px` : 'var(--Grid_Gutter)'

          return `calc((${columns} / ${totalColumns} * 100%) - (${gutter} * 2) * (${totalColumns} - ${columns}) / ${totalColumns})`
        },
        columnsandgutter: (columns, totalColumns, gutter) => {
          gutter = gutter ? `${gutter}px` : 'var(--Grid_Gutter)';

          return `calc((${columns} / ${totalColumns} * 100%) - (${gutter} * 2) * (${totalColumns} - ${columns}) / ${totalColumns} + (${gutter} * 2))`;
        },
        'smooth-gradient': (
          direction,
          startingColor,
          finalColor,
          easingFunction = 'ease',
          stops = 5,
          colorMode = ''
        ) => {
          // Code  adapted from the easing-gradients PostCSS plugin here:
          // https://github.com/larsenwork/postcss-easing-gradients
          //
          // Simple usage:
          //
          // background-image: smooth-gradient(to right, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0))
          //
          const chroma = require('chroma-js');
          const easingCoordinates = require('easing-coordinates');

          // Change 'transparent' into a transparent version of the starting color
          let colors = [startingColor, finalColor];
          colors = colors.map((color, i) => {
            return color === 'transparent'
              ? chroma(colors[Math.abs(i - 1)])
                  .alpha(0)
                  .css('hsl')
              : color;
          });

          // Get the stops for the gradient using the easing function.
          const coordinates = easingCoordinates.easingCoordinates(
            easingFunction,
            stops - 1
          );

          // Go through the coordinates and give them the colours for that stop.
          const colorStops = [];
          const alphaDecimals = 2;
          coordinates.forEach(coordinate => {
            const ammount = coordinate.y;
            const percent = coordinate.x * 100;
            let color = chroma
              .mix(colors[0], colors[1], ammount, colorMode)
              .css('hsl');

            // Round the colours to the nearest 'alphaDecimals' decimal places
            const prefix =
              color.indexOf('(') !== -1
                ? color.substring(0, color.indexOf('('))
                : color;
            const values = color
              .match(/\((.*)\)/)
              .pop()
              .split(',')
              .map(string =>
                string.indexOf('%') === -1
                  ? +Number(string).toFixed(alphaDecimals)
                  : string.trim()
              );

            // Pair the colour stop with the co-ords
            color = `${prefix}(${values.join(', ')})`;

            // Add the new pair to the main output array. We don't need the stop % for the first and last items in the list.
            if (Number(coordinate.x) !== 0 && Number(coordinate.x) !== 1) {
              colorStops.push(`${color} ${+percent.toFixed(2)}%`);
            } else {
              colorStops.push(color);
            }
          });
          return `linear-gradient(${direction}, ${colorStops.join(', ')})`;
        }
      }
    },
    'postcss-custom-properties': {
      preserve: false
    },
    'postcss-custom-media': {},
    'postcss-media-minmax': {},
    'postcss-assets': {
      basePath: '{{cookiecutter.package_name}}/assets/',
      loadPaths: ['img/'],
      baseUrl: '/static/'
    },
    'postcss-property-lookup': {},
    'postcss-pxtorem': {},
    'postcss-will-change': {},
    'postcss-round-subpixels': {},
    'postcss-hexrgba': {},
    'autoprefixer': {},
    'postcss-preset-env': {
      browsers: 'last 2 versions',
    },
    'cssnano': {},
  },
};
