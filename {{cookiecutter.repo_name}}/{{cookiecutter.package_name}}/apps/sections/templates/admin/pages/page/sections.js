(function ($) {
  document.addEventListener('DOMContentLoaded', function() {
    // The timeout is necessary so that Jet can load fully.
    window.setTimeout(renderSectionFields, 1)

    var sectionSelector = '[id*="section_set"].inline-related'

    $(document).on("change", sectionSelector + " .field-type select", renderSectionFields);
    // Once again, this is on a timeout so the fields get a chance to render.
    $('.inline-navigation, .changeform-tabs-item').on('click', function () {
      window.setTimeout(renderSectionFields, 1)
    })


    function renderSectionFields() {
      var $sections = $(sectionSelector);

      var types = {
        '': {
          'fields': [],
          'required': [],
          'helpText': {}
        },
      {% for type in types %}
        '{{ type.slug }}': {
          'fields': {{ type.fields|default:'[]'|safe }},
          'required': {{ type.required|default:'[]'|safe }},
          'helpText': {{ type.help_text | default:'{}'|safe }}{% if not forloop.last %},{% endif %}
        }{% if not forloop.last %},{% endif %}
      {% endfor %}
      };

      $sections.each(function () {
        // Define our section
        var $section = $(this);

        // We get the select so we can exclude it from the fields list and we can
        // also check if it has a value to see if hidden fields should be rendered
        var $select = $('.field-type select', $section);

        // These are the fields we will be unhiding
        var fieldsToShow = types[$select.val()].fields;
        var requiredFields = types[$select.val()].required;
        var helpText = types[$select.val()].helpText;

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

        if (requiredFields) {
          var fieldClassNames = requiredFields.map(function (field) { return 'field-' + field })

          $.each($fields, function (index, field) {
            var $field = $(field);
            var name = $field.attr('class').split(' ').filter(function(name) { return name.indexOf('field-') >= 0 })[0];
            var isRequired = fieldClassNames.indexOf(name) >= 0;

            $field.find('label').toggleClass('required', isRequired);
            $field.find('input, textarea, select').prop('required', isRequired);
          })
        }

        $.each($fields, function (index, field) {
          var $helpText = $($(field).find('.help-inline'));
          var helpTextExists = $helpText.length > 0;

          if ($(field).data('help-text') === undefined) {
            $(field).data('help-text', helpTextExists);

            if (helpTextExists) {
              $helpText.data('help-text-default', $helpText.text());
            }
          }
        });

        $.each($fields, function (index, field) {
          var $helpText = $($(field).find('.help-inline'));
          var helpTextExists = $helpText.length > 0;
          var hasHelpTextByDefault = $(field).data('help-text') === true;
          var name = $(field)
            .attr('class')
            .split(' ')
            .filter(function(name) { return name.indexOf('field-') >= 0 })[0]
            .replace('field-', '');
          if (name in helpText) {
            if (helpTextExists) {
              $helpText.text(helpText[name]);
            } else {
              $('<div><span class="help-inline">' + helpText[name] + '</span></div>')
                .appendTo($(field).find('.controls'));
            }
          } else {
            if (hasHelpTextByDefault && helpTextExists) {
              $helpText.text($helpText.data('help-text-default'));
            } else if (hasHelpTextByDefault === false) {
              $helpText.remove();
            }
          }
        });

        $('.wysiwyg:visible', $section).each(function (index, field) {
          activate_tinymce(field)
        });
      });
    }
  })
})(window.jQuery);
