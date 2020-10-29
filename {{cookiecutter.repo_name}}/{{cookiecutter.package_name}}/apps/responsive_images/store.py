from django.core.cache import cache

from .conf import settings
from .models import ThumbnailData


class OptionStore:
    def __init__(self, cache_prefix=settings.RESPONSIVE_IMAGES_CACHE_PREFIX):
        if not cache_prefix:
            raise TypeError("'cache_prefix' cannot be empty.")
        self._cache_prefix = cache_prefix

    @property
    def cache_prefix(self):
        if callable(self._cache_prefix):
            return self._cache_prefix()
        return self._cache_prefix

    def _get_key(self, key):
        return f'{self.cache_prefix}{key}'

    def get(self, key):
        cache_key = self._get_key(key)
        cached_options = cache.get(cache_key)
        if cached_options:
            if isinstance(cached_options, ThumbnailData):
                return cached_options
            cache.delete(cache_key)
        return ThumbnailData.objects.filter(pk=key).first()

    def set(self, obj):
        cache_key = self._get_key(obj.pk)
        obj.save()
        cache.set(cache_key, obj, None)

    def flush(self):
        images = ThumbnailData.objects.filter(pk__startswith=self.cache_prefix)
        key_list = images.values_list('key')
        for key in key_list:
            cache.delete(self._get_key(key))
        images.delete()


option_store = OptionStore()
