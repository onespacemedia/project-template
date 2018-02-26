from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


class HasImageAdminMixin(object):
    '''
    A helper to add a thumbnail into admin list views, for models that have an
    ImageRefField field.

    Inherit from this and add `get_image` to your `list_display` in the place
    you want to show the image. If you have the image set as the first column
    in the list, you'll probably want to override `list_display_links` as
    well.

    class MyModelAdmin(HasImageAdminMixin, admin.ModelAdmin):
        list_display = ['get_image', '__str__']
        list_display_links = ['get_image', '__str__']

    It assumes that the field is called "image"; if it's called something else
    on your model, override the `image_field` attribute, e.g.:

    class MyModelAdmin(HasImageAdminMixin, admin.ModelAdmin):
        image_field = 'photo'
    '''
    image_field = 'image'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(self.image_field)

    def get_image(self, obj):
        """Generates a thumbnail of the image."""
        image = getattr(obj, self.image_field)
        if not image:
            return ''
        try:
            thumbnail = get_thumbnailer(image.file).get_thumbnail({'size': (100, 66), 'quality': 99})
            return mark_safe('<img src="{}" width="{}" height="{}" alt=""/>'.format(
                thumbnail.url,
                thumbnail.width,
                thumbnail.height,
            ))
        except:  # pylint:disable=bare-except
            # ^^ We allow bare exceptions above because of the vast number
            # of exceptions that can occur; it could be IOError for bad
            # permissions, ValueError or ZeroDivisionError with invalid files,
            # etc.
            return '(corrupt image?)'
    get_image.short_description = 'Image'
