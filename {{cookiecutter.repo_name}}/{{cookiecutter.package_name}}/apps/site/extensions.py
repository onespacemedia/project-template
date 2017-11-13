from datetime import datetime

from django.conf import settings
from django.utils.formats import date_format
from django.utils.timezone import get_current_timezone
from jinja2 import lexer, nodes
from jinja2.ext import Extension


class DjangoNow(Extension):
    """
    Implements django's `{% now %}` tag.
    """
    tags = set(['now'])

    def _now(self, format_string):
        tzinfo = get_current_timezone() if settings.USE_TZ else None
        cur_datetime = datetime.now(tz=tzinfo)

        return date_format(cur_datetime, format_string)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        token = parser.stream.expect(lexer.TOKEN_STRING)
        format_string = nodes.Const(token.value)
        call = self.call_method('_now', [format_string], lineno=lineno)

        token = parser.stream.current
        if token.test('name:as'):
            next(parser.stream)
            as_var = parser.stream.expect(lexer.TOKEN_NAME)
            as_var = nodes.Name(as_var.value, 'store', lineno=as_var.lineno)
            return nodes.Assign(as_var, call, lineno=lineno)

        return nodes.Output([call], lineno=lineno)
