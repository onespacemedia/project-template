from django.http import Http404
from django.views.generic import RedirectView
from sorl.thumbnail import get_thumbnail

from .store import option_store


class DeferredThumbnailView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        key = kwargs.get('key')

        thumbnail_data = option_store.get(key)
        if thumbnail_data:
            options = thumbnail_data.options

            file_ = thumbnail_data.media_file

            thumbnail = get_thumbnail(file_, **options)

            if not thumbnail_data.rendered:
                thumbnail_data.rendered = True

                option_store.set(thumbnail_data)

            return thumbnail.url
        raise Http404('Thumbnail data not found.')
