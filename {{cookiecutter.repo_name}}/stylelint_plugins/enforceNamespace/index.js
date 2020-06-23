/* eslint-disable no-var,prefer-template, object-shorthand */
var stylelint = require('stylelint')
var ruleName = 'osm/enforce-namespace'

var messages = stylelint.utils.ruleMessages(ruleName, {
  noNamespace: (file) => 'No namespace found for file',
  wrongNamespace: (selector, appName) => 'Selector "' + selector + '" doesn\'t use that file\'s namespace ' + appName
})

function findTopParentSelector (node) {
  if (node.parent.type === 'root' || node.parent.type === 'atrule') {
    return node.selector
  } else {
    return findTopParentSelector(node.parent)
  }
}

function isInsideAtRule (node) {
  if (node.parent.type === 'atrule') {
    return true
  } else if (node.parent.type === 'root') {
    return false
  } else {
    return findTopParentSelector(node.parent)
  }
}

module.exports = stylelint.createPlugin(ruleName, function (max, options) {
  return function (root, result) {
    var namespaceLoc = root.source.input.css.indexOf('@namespace')
    if (namespaceLoc === -1) {
      var isEmpyFile = true

      for (node of root.nodes) {
        if (node.type === 'rule') {
          isEmpyFile = false
        }
      }

      if (!isEmpyFile) {
        stylelint.utils.report({
          ruleName: ruleName,
          result: result,
          line: 1,
          message: messages.noNamespace()
        })
      }

      return
    }

    var namespaceStart = root.source.input.css.indexOf(' ', namespaceLoc)
    var namespaceEnd = root.source.input.css.indexOf('\n', namespaceLoc)
    var namespace = root.source.input.css.substring(namespaceStart + 1, namespaceEnd)
    if (namespace.indexOf('.') === -1) {
      namespace = '.' + namespace
    }

    root.walkRules(rule => {
      if (isInsideAtRule(rule)) return
      const topParentSelector = findTopParentSelector(rule)
      if (topParentSelector.indexOf(namespace, 0) !== 0) {
        stylelint.utils.report({
        ruleName: ruleName,
        result: result,
        node: rule,
        message: messages.wrongNamespace(topParentSelector, namespace)
      })
      }
    })
  }
})

module.exports.ruleName = ruleName
module.exports.messages = messages
