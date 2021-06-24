CONFIG = {
    'category': 'Heroes',
    'name': 'Landing hero',
    'fields': [
        'background_colour', 'top_padding', 'bottom_padding',
        'icon', 'kicker', 'title', 'text', 'image', 'link_text',
        'link_page', 'link_url', 'secondary_link_text',
        'secondary_link_page', 'secondary_link_url'
    ],
    'search': ['kicker', 'title', 'text'],
    'required': ['title', 'image'],
    'help_text': {
        'kicker': 'If this is left blank it will inherit the title of the page.',
    },
}
