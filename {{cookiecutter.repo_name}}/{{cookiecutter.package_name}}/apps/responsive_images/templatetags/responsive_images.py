# pylint: disable=too-many-arguments, too-many-locals
from django.urls import reverse
from django_jinja import library
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.helpers import tokey
from sorl.thumbnail.images import BaseImageFile

from ..conf import settings
from ..models import ThumbnailData
from ..store import OptionStore

option_store = OptionStore()


@library.global_function
@library.render_with('responsive_images/wrapped-image.html')
def render_osm_lazy_image(*args, **kwargs):
    return get_image_data(*args, **kwargs)


@library.global_function
@library.render_with('responsive_images/wrapped-image.html')
def render_image(*args, **kwargs):
    return get_image_data(*args, **kwargs)


@library.global_function
@library.render_with('responsive_images/picture.html')
def render_simple_image(*args, **kwargs):
    return get_image_data(*args, **kwargs)


class DeferredImage(BaseImageFile):
    def __init__(self, file_, width, height, key):
        self.size = [width or file_.width, height or file_.height]
        self.name = file_.title
        self.key = key

    def exists(self):
        return False

    @property
    def url(self):
        return reverse('deferred_image', kwargs={
            'key': self.key,
        })

    src = url

    def __str__(self):
        return self.name


def get_sourceset(image, width=None, height=None, max_width=settings.RESPONSIVE_IMAGES_MAX_WIDTH,
                  max_height=settings.RESPONSIVE_IMAGES_MAX_HEIGHT, crop='center', pixel_densities=(2,),
                  normal_quality=settings.RESPONSIVE_IMAGES_QUALITY,
                  webp_quality=settings.RESPONSIVE_IMAGES_QUALITY_WEBP,
                  webp=settings.RESPONSIVE_IMAGES_ENABLE_WEBP, defer=settings.RESPONSIVE_IMAGES_DEFER_GENERATION,
                  **sorl_options):

    pixel_densities = set(pixel_densities)
    user_sized = width and height
    intrinsic_width = width if user_sized else image.width
    intrinsic_height = height if user_sized else image.height
    aspect_ratio = intrinsic_height / intrinsic_width
    aspect_ratio_percentage = f'{aspect_ratio * 100}%'

    if max_width:
        width = width or intrinsic_width
        if width > max_width:
            if user_sized:
                height = int(width * aspect_ratio)
            width = max_width

    if max_height:
        height = intrinsic_height
        if height > max_height:
            if user_sized:
                width = int(height / aspect_ratio)
            height = max_height

    # Gets thumbnail geometry to pass to sorl e.g '500x200'
    # Takes width, height and pixel density as args
    get_sorl_geometry = lambda w, h, f=1: (str(int(w * f)) if w else '') + (f'x{int(h*f)}' if h else '')

    def get_deferred_thumbnail(file_, geometry_string, **kwargs):
        options = list(kwargs.values())
        key = tokey(file_, geometry_string, *options)

        thumbnail_data = option_store.get(key)
        if thumbnail_data:
            if thumbnail_data.rendered:
                return get_thumbnail(file_, geometry_string, **kwargs)
        else:
            image_options = ThumbnailData.create(key, image.file, dict(geometry_string=geometry_string, **kwargs))

            option_store.set(image_options)

        return DeferredImage(image, width, height, key)

    if defer:
        thumbnail_function = get_deferred_thumbnail
    else:
        thumbnail_function = get_thumbnail

    base_geometry = get_sorl_geometry(width, height)
    source_options = dict(crop=crop, quality=normal_quality, **sorl_options)
    source_thumbnail = thumbnail_function(image.file, base_geometry, **source_options)

    source_image = {
        '1': source_thumbnail
    }

    webp_options = dict(crop=crop, quality=webp_quality, format='WEBP', **sorl_options)

    webp_image = None
    if webp:
        webp_thumbnail = thumbnail_function(image.file, base_geometry, **webp_options)
        webp_image = {
            '1': webp_thumbnail,
        }

    for factor in pixel_densities:
        geometry = get_sorl_geometry(width, height, factor)
        key = str(factor)
        source_image[key] = thumbnail_function(image.file, geometry, **sorl_options)
        if webp:
            webp_image[key] = thumbnail_function(image.file, geometry, **webp_options)

    return {
        'width': source_thumbnail.width,
        'height': source_thumbnail.height,
        'aspect_ratio': aspect_ratio_percentage,
        'source_image': source_image,
        'webp_image': webp_image,
    }


def get_image_data(image, width=None, height=None, blur=False, show_small_image=False, loading='lazy',
                   image_options=None, alt_text=None, **kwargs):
    def get_small_dimensions(w, h, factor=20.0, threshold=200):
        if w > threshold and h > threshold:
            return int(round(w / factor)), int(round(h / factor))
        return None, None

    def get_quality_kwargs(quality):
        quality_kwargs = {}
        if quality:
            if isinstance(quality, int):
                quality_kwargs['normal_quality'] = quality_kwargs['webp_quality'] = quality
            elif isinstance(quality, dict):
                if 'normal' in quality:
                    quality_kwargs['normal_quality'] = quality['normal']
                if 'webp' in quality:
                    quality_kwargs['webp_quality'] = quality['webp']
            else:
                raise TypeError("'quality' must be an 'int' or 'dict' instance.")
        return quality_kwargs

    loading_options = ['lazy', 'eager', 'auto']

    if loading not in loading_options:
        quote = lambda s: f"'{s}'"
        raise ValueError(
            f"Incorrect value {loading} given for 'loading'. Choices are {', '.join(map(quote, loading_options))}")

    webp = kwargs.get('webp', settings.RESPONSIVE_IMAGES_ENABLE_WEBP)

    small_image = None
    default = None

    kwargs.update(get_quality_kwargs(kwargs.pop('quality', None)))

    image_options = image_options or []

    processed_images = []
    for item in image_options:
        if not item:
            raise TypeError("At least one option is required for each item in 'image_options'")
        if 'webp' in item:
            raise TypeError("'webp' can only be given as a base argument, not in 'image_options'")

        media = item.pop('media', 'default')

        image_arguments = kwargs.copy()
        item['image'] = item.get('image', image)
        image_arguments.update(item)
        image_arguments.update(get_quality_kwargs(item.pop('quality', None)))
        processed = get_sourceset(**image_arguments)

        if media == 'default':
            # We keep the default image separately from the list of media images
            default = processed
            continue

        processed['media'] = settings.RESPONSIVE_IMAGES_MEDIA_DEFINITIONS[media]
        processed_images.append(processed)

    if not default:
        default = get_sourceset(image, width=width, height=height, **kwargs)

    if show_small_image:
        small_image_width, small_image_height = get_small_dimensions(default['width'], default['height'])
        # There's no point having a small image if our image is already small
        show_small_image = small_image_width and small_image_height
        if show_small_image:
            small_image = get_sourceset(
                image,
                small_image_width,
                small_image_height,
                normal_quality=100,
                pixel_densities=[],
            )

    return {
        'alt_text': alt_text or image.alt_text or '',
        'blur': blur,
        'default': default,
        'images': processed_images,
        'is_transparent': str(image.file).endswith('.png'),
        'loading': loading,
        'small_image': small_image,
        'webp': webp,
    }
