'''Miscellaneous helpful functions.'''


def get_related_items(candidate_querysets, count=3, exclude=None):
    '''
    Returns `count` related items for an object given one or more candidate
    querysets. `exclude` should be an object you would like to exclude; for
    example, if you are trying to get similar news articles for a certain
    article, you will want to pass the article in question as the `exclude`
    parameter.

    An example from the news app:

    def get_related_articles(self, count=3):
        candidate_querysets = [
            Article.objects.filter(categories__in=self.categories.all()),
            Article.objects.all(),
        ]
        return get_related_items(candidate_querysets, count=count, exclude=self)
    '''
    objects = []

    for candidate_queryset in candidate_querysets:
        if exclude:
            candidate_queryset = candidate_queryset.exclude(pk=exclude.pk)

        objects += list(
            candidate_queryset.exclude(
                pk__in=[obj_existing.pk for obj_existing in objects]
            ).distinct()[:count - len(objects)]
        )

        if len(objects) >= count:
            break

    return objects
