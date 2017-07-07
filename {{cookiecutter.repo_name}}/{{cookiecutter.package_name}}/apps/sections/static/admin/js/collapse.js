(function($) {
  $(document).ready(function() {
    // Add anchor tag for Show/Hide link
    $("fieldset.collapse, .inline-related.collapse").each(function(i, elem) {
      // Don't hide if fields in this fieldset have errors
      if ($(elem).find("div.errors").length == 0) {
        $(elem).addClass("collapsed").find("h2, h3").first().append(' (<a id="fieldsetcollapser' +
          i +'" class="collapse-toggle" href="#">' + gettext("Show") +
          '</a>)');
      }
    });
    // Add toggle to anchor tag
    $("fieldset.collapse a.collapse-toggle, .inline-related.collapse a.collapse-toggle").click(function(ev) {
      if ($(this).closest("fieldset, .inline-related").hasClass("collapsed")) {
        // Show
        $(this).text(gettext("Hide")).closest("fieldset, .inline-related").removeClass("collapsed").trigger("show.fieldset", [$(this).attr("id")]);
      } else {
        // Hide
        $(this).text(gettext("Show")).closest("fieldset, .inline-related").addClass("collapsed").trigger("hide.fieldset", [$(this).attr("id")]);
      }
      return false;
    });
  });
})(django.jQuery);
