window.jQuery(function () {
  setInterval(hide_inline_section_fields, 100)
});

function hide_inline_section_fields () {
  var options = document.querySelector('#id_type').querySelectorAll('option');
  var optionSet = new Set();
  var optionSelected = document.querySelector('.select2-selection__rendered').innerHTML.toLowerCase();
  for (var i = 0; i < options.length; i++) {
    // Catch the case options[i].value = '', which is when no settings type chosen
    if (options[i].value) {
      optionSet.add(options[i].value)
    }
  }

  var formFields = document.querySelectorAll('.form-row');
  var fieldInput = document.querySelector('body');
  for (i = 0; i < formFields.length; i++) {
    fieldInput = formFields[i].querySelector('input');
    if (!fieldInput) {
      fieldInput = formFields[i].querySelector('textarea');
    }
    if (fieldInput && fieldInput.id) {
      if (optionSet.has(fieldInput.id.substring(3))) {
        formFields[i].style.display = 'none'
      }

      if (fieldInput.id.substring(3) === optionSelected) {
        formFields[i].style.display = 'block'
      }
    }
  }
}
