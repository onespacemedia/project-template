$(window).load(function() {
  var $sections = $('div[class*="section_set"]');

  renderSectionFields();

  $sections.find('.field-type select').change(renderSectionFields);

  $(document).on("change", "[class*=section_set] .field-type select", renderSectionFields);
  // As jQuery event bindings are 'first come first served',
  // showHideSectionFields will be called after the default 'add another
  // section' handler is called. So this will work!
  // (It'll also be fired when *any* 'add another' button is pressed, but)
  // this is harmless.)
  $(".add-row a").click(renderSectionFields);

  function renderSectionFields() {
    var $sections = $('div[class*="section_set"]');

    var types = {
      '': [],
      {% for type in types %}
      '{{ type.name }}': {{ type.fields|default:'[]'|safe }}{% if not forloop.last %},{% endif %}
      {% endfor %}
    };

    $sections.each(function () {
      // Define our section
      var $section = $(this);

      // We get the select so we can exclude it from the fields list and we can
      // also check if it has a value to see if hidden fields should be rendered
      var $select = $('.field-type select', $section);

      // These are the fields we will be unhiding
      var fieldsToShow = types[$select.val()];

      // Get all of the fields in the section
      var $fields = $('div[class*="field-"]', $section);

      // Remove the fields we want on every section
      $fields = $fields.not('.field-type, .field-order');

      // Hide all the fields initially
      $fields.hide();

      // If there are fields to show, show them!
      if (fieldsToShow) {
        $.each(fieldsToShow, function (index, field) {
          $section.find('.field-' + field).show();
        });
      }
    });
  }
});
