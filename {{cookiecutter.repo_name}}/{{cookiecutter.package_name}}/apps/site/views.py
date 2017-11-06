from cms.apps.media.models import File
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from sorl.thumbnail import get_thumbnail


class ImageView(RedirectView):
    # If they change the source image, we don't want to be showing the old image.
    # Sorl uses memcached to retrieve images with the same args, so this should
    # be pretty quick.
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # kwargs:
        # {'pk': '9', 'width': '285', 'height': '400', 'format': 'webp', 'crop': 'None'}
        file_ = get_object_or_404(File, pk=kwargs['pk'])

        sorl_args = [
            file_.file,
        ]
        sorl_kwargs = {}

        dimensions = ''
        width = kwargs['width']
        height = kwargs['height']

        if width == 'auto':
            dimensions = f'x{height}'
        elif height == 'auto':
            dimensions = width
        else:
            dimensions = f'{width}x{height}'

            if 'crop' not in kwargs:
                kwargs['crop'] = 'center'

        sorl_args.append(dimensions)

        if kwargs['crop'].lower() != 'none':
            sorl_kwargs['crop'] = kwargs['crop']

        if kwargs['format'] != 'source':
            sorl_kwargs['format'] = kwargs['format'].upper()

        return get_thumbnail(
            *sorl_args,
            **sorl_kwargs
        ).url
