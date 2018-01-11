import urllib

import requests
from bs4 import BeautifulSoup


def get_oembed_info_url(url):
    '''A helper to get the oEmbed information URL for a video.

    This special-cases YouTube videos because bot requests to video pages
    frequently result in the IP being captcha'd out, which breaks the
    auto-discovery mechanism. Fortunately, these IP bans do not seem to apply
    to requests to `/oembed`.
    '''
    youtube_domains = ['youtu.be', 'www.youtube.com', 'youtube.com', 'm.youtube.com']

    if urllib.parse.urlparse(url).netloc in youtube_domains:
        return 'https://www.youtube.com/oembed?format=json&{}'.format(
            urllib.parse.urlencode({'url': url})
        )

    # The "not YouTube" case - this should reliably handle everything
    # including Vimeo.
    try:
        req = requests.get(url)
        text = req.text
        soup = BeautifulSoup(text, 'html.parser')
    except:  # pylint:disable=bare-except
        # Either requests failed, or it looked nothing like HTML.
        return

    # Video providers that support oEmbed will have something that looks like
    # this:
    # <link rel='alternate' type='application/json+oembed' href='...'>
    # Where the contents of 'href' tell us where to go to get JSON
    # for an embed code.
    try:
        rel_tag = soup.find(attrs={
            'type': 'application/json+oembed'
        })
        assert rel_tag.get('href')
    except:  # pylint:disable=bare-except
        # This can probably happen if a video is private or deleted.
        return

    # Now, let's grab the JSON
    return rel_tag.get('href')


def get_video_info(url):
    '''Returns video information for a given URL. Returns a dict in this form:

    {
        'embed_code': '<iframe src=...>',
        'title': 'Title of a video',
    }

    ...or None if no information could be found.
    '''

    if not url or (not url.startswith('http://') and not url.startswith('https://')):
        return

    oembed_url = get_oembed_info_url(url)
    if not oembed_url:
        return

    try:
        req = requests.get(oembed_url)
        json = req.json()
    except:  # pylint:disable=bare-except
        # Bare exception because a lot of possible errors could
        # happen here. Not just requests.exception.RequestException -
        # there's all the ones that could happen in the json library
        # too.
        return

    # Sanity check.
    if 'html' not in json or not json['html']:
        return

    return {
        'embed_code': json['html'],
        'title': json['title'],
    }


def get_video_iframe_url(url, modest=False):
    info = get_video_info(url)

    if not info:
        return

    soup = BeautifulSoup(info['embed_code'], 'html.parser')
    src = soup.find('iframe')['src']
    # Remove query string - if we need extra stuff like '?autoplay=1' we
    # can add it later.
    if src.find('?') > -1:
        src = src[:src.find('?')]
    return src
