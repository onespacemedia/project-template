module.exports = {
  'plugins': [
    'stylelint-statement-max-nesting-depth'
  ],
  'rules': {
    // Plugins
    'statement-max-nesting-depth': [3, {
      countAtRules: false,
      countedNestedAtRules: false
    }],

    // String
    'string-quotes': 'single',

    // Color
    'color-hex-case': 'lower',
    'color-hex-length': 'short',
    'color-no-invalid-hex': true,
    'color-no-named': true,

    // Number
    'number-leading-zero': 'always',
    'number-max-precision': 2,
    'number-no-trailing-zeros': true,
    'number-zero-length-no-unit': true,

    // Function
    'function-calc-no-unspaced-operator': true,
    'function-comma-space-after': 'always',
    'function-comma-space-before': 'never',
    'function-linear-gradient-no-nonstandard-direction': true,
    'function-url-quotes': 'single',

    // Value
    'value-no-vendor-prefix': true,

    // Value list
    'value-list-comma-space-after': 'always',
    'value-list-comma-space-before': 'never',

    // Unit
    'unit-blacklist': ['em', 'rem'], // Disallow these because PostCSS adds them

    // Declaration
    'declaration-bang-space-after': 'never',
    'declaration-bang-space-before': 'always',
    'declaration-colon-space-after': 'always',
    'declaration-colon-space-before': 'never',
    'declaration-no-important': true, // Ask DG if this is causing you problems

    // Declaration block
    'declaration-block-semicolon-newline-after': 'always-multi-line',
    'declaration-block-semicolon-space-after': 'always-single-line',

    // Block
    'block-closing-brace-newline-after': 'always',
    'block-closing-brace-newline-before': 'always-multi-line',
    'block-closing-brace-space-before': 'always-single-line',
    'block-no-empty': true,
    'block-opening-brace-newline-after': 'always-multi-line',
    'block-opening-brace-space-after': 'always-single-line',
    'block-opening-brace-space-before': 'always',

    // Selector
    'selector-combinator-space-after': 'always',
    'selector-combinator-space-before': 'always',
    'selector-no-id': true,
    'selector-no-type': true, // Ask DG if this is causing you problems
    'selector-no-universal': true,
    'selector-no-vendor-prefix': true,
    'selector-pseudo-element-colon-notation': 'double',

    // Selector list
    'selector-list-comma-space-after': 'always-single-line',
    'selector-list-comma-space-before': 'never',

    // Rules
    'rule-nested-empty-line-before': ['always', {
      except: ['first-nested'],
      ignore: ['after-comment']
    }],
    'rule-no-duplicate-properties': true,
    'rule-no-shorthand-property-overrides': true,
    'rule-non-nested-empty-line-before': ['always-multi-line', {
      ignore: ['after-comment']
    }],
    'rule-properties-order': [
      {
        emptyLineBefore: true,
        properties: [
          'content'
        ]
      },
      {
        emptyLineBefore: true,
        properties: [
          'position',
          'top',
          'right',
          'bottom',
          'left',
          'z-index'
        ]
      },
      {
        emptyLineBefore: true,
        properties: [
          'align-content',
          'align-items',
          'align-self',
          'flex',
          'flex-basis',
          'flex-direction',
          'flex-flow',
          'flex-grow',
          'flex-shrink',
          'flex-wrap',
          'justify-content',
          'order'
        ]
      },
      {
        emptyLineBefore: true,
        properties: [
          'display',
          'float',
          'height',
          'margin',
          'margin-top',
          'margin-right',
          'margin-bottom',
          'margin-left',
          'max-height',
          'max-width',
          'min-height',
          'min-width',
          'padding',
          'padding-top',
          'padding-right',
          'padding-bottom',
          'padding-left',
          'table-layout',
          'width'
        ]
      },
      {
        emptyLineBefore: true,
        properties: [
          'font-family',
          'font-size',
          'font-style',
          'font-weight',
          'letter-spacing',
          'line-height',
          'text-align',
          'text-decoration',
          'text-overflow'
        ]
      },
      {
        emptyLineBefore: true,
        properties: [
          'background',
          'background-attachment',
          'background-color',
          'background-image',
          'background-position',
          'background-repeat',
          'background-size',
          'border',
          'border-top',
          'border-right',
          'border-bottom',
          'border-left',
          'border-radius',
          'border-top-left-radius',
          'border-top-right-radius',
          'border-bottom-right-radius',
          'border-bottom-left-radius',
          'box-shadow',
          'color',
          'cursor',
          'opacity',
          'overflow',
          'overflow-x',
          'overflow-y',
          'visibility'
        ]
      },
      {
        emptyLineBefore: true,
        properties: [
          'animation',
          'animation-delay',
          'animation-direction',
          'animation-duration',
          'animation-fill-mode',
          'animation-iteration-count',
          'animation-name',
          'animation-play-state',
          'animation-timing-function',
          'transform',
          'transition'
        ]
      }
    ],
    'rule-trailing-semicolon': 'always',

    // Media
    'media-feature-colon-space-after': 'always',
    'media-feature-colon-space-before': 'never',
    'media-feature-name-no-vendor-prefix': true,
    'media-feature-range-operator-space-after': 'always',
    'media-feature-range-operator-space-before': 'always',

    // Custom media
    'custom-media-pattern': 'xs|sm|md|lg|xlg|xxlg.+/',

    // Media query
    'media-query-parentheses-space-inside': 'never',

    // At rule
    'at-rule-empty-line-before': ['always', {
      except: ['blockless-group', 'first-nested'],
      ignore: ['after-comment']
    }],
    'at-rule-no-vendor-prefix': true,

    // Comment
    'comment-whitespace-inside': 'always',

    // General
    'indentation': 2,
    'no-eol-whitespace': true,
    'no-missing-eof-newline': true
  }
}
