module.exports = {
  root: true,
  extends: ['standard'],
  parser: 'babel-eslint',
  parserOptions: {
    sourceType: 'module',
    allowImportExportEverywhere: true
  },
  plugins: ['compat', 'html', 'prettier'],
  env: {
    browser: true,
    es6: true
  },
  rules: {
    'compat/compat': 2,
    'no-new': [0],
    'no-var': [2],
    'object-shorthand': [2, 'always'],
    'prefer-const': [1],
    'prefer-template': [2],
    'no-console': [2],
    'no-unused-vars': [1]
  }
}
