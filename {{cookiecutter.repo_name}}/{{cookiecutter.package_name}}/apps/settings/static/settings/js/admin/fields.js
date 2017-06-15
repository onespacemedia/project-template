$(function () {
  setInterval(hide_inline_section_fields, 100)
})

//	Function to hide fields of a section inline based on its type
function hide_inline_section_fields () {
  //	Define which section types have which elements
  var elements = {
    '.field-string': ['string'],
    '.field-text': ['text'],
    '.field-number': ['number'],
    '.field-image': ['image']
  }

  //	Loop all of the section inlines
  $('.tab-content').each(function () {
    var _this = this

    //	Get the type select of the section
    var select = $('[id$=_type]', $(this))[0].value
    select = select == '' ? '0' : select

    //	Loop the elements
    for (var element in elements) {
      var element_object = $(element, $(this))

      // Hide / show the element based on select index
      if (elements[element].indexOf(select) != -1) {
        element_object.css('display', '')
      } else {
        element_object.css('display', 'none')
      }
    }
  })
}
