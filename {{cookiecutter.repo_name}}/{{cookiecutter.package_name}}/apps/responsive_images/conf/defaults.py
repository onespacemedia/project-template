RESPONSIVE_IMAGES_DEFER_GENERATION = True

RESPONSIVE_IMAGES_QUALITY = 60
RESPONSIVE_IMAGES_QUALITY_WEBP = 80

RESPONSIVE_IMAGES_MAX_WIDTH = 1920
RESPONSIVE_IMAGES_MAX_HEIGHT = None

# This is the namespace you gave the package in your urls.py
RESPONSIVE_IMAGES_URL_NAMESPACE = 'assets'

# Do you want the lazy images to server webp where possible?
RESPONSIVE_IMAGES_ENABLE_WEBP = True

RESPONSIVE_IMAGES_MEDIA_DEFINITIONS = {
    'xxs': '(max-width: 450px)',
    'xs': '(max-width: 768px)',
    'sm': '(max-width: 900px)',
    'md': '(max-width: 1200px)',
    'lg': '(max-width: 1440px)',
}

RESPONSIVE_IMAGES_CACHE_PREFIX = 'osm-images-'
