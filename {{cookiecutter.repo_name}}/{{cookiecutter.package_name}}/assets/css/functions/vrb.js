module.exports = function(val) {
  // 12 is taken from the --VerticalRhythmBaseline in property-definitions.css
  return String(12 * val) + 'px'
}
