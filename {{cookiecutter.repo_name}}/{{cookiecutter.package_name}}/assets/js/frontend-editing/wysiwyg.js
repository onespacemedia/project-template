import tinymce from 'tinymce/tinymce'
import 'tinymce/plugins/advlist/plugin'
import 'tinymce/plugins/anchor/plugin'
import 'tinymce/plugins/autolink/plugin'
import 'tinymce/plugins/charmap/plugin'
import 'tinymce/plugins/code/plugin'
import 'tinymce/plugins/colorpicker/plugin'
import 'tinymce/plugins/contextmenu/plugin'
import 'tinymce/plugins/directionality/plugin'
import 'tinymce/plugins/fullscreen/plugin'
import 'tinymce/plugins/hr/plugin'
import 'tinymce/plugins/image/plugin'
import 'tinymce/plugins/link/plugin'
import 'tinymce/plugins/lists/plugin'
import 'tinymce/plugins/pagebreak/plugin'
import 'tinymce/plugins/paste/plugin'
import 'tinymce/plugins/table/plugin'
import 'tinymce/plugins/template/plugin'
import 'tinymce/plugins/textcolor/plugin'
import 'tinymce/plugins/textpattern/plugin'
import 'tinymce/plugins/visualblocks/plugin'
import 'tinymce/plugins/visualchars/plugin'
import 'tinymce/plugins/wordcount/plugin'
import 'tinymce/themes/modern/theme'

export default function ({ selector }) {
  tinymce.baseURL = '/static/tinymce'
  const settings = JSON.parse(document.querySelector(selector).dataset.wysSettings)
  settings.selector = selector

  tinymce.init(settings)
}
