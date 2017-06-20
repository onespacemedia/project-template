module.exports = function (val1, val2) {
  var number = val1 / val2 * 100

  return number.toFixed(2) + '%'
}
