from django.contrib import admin
from osm_jet.admin import JetCompactInline
from reversion.admin import VersionAdmin

from ...utils.admin import LinkFieldsLastAdminMixin, UsedOnAdminMixin
from .models import (CallToAction, Card, CardSet, Link, LinkSet, Sidebox,
                     Statistic, StatSet)


@admin.register(CallToAction)
class CallToActionAdmin(LinkFieldsLastAdminMixin, admin.ModelAdmin, UsedOnAdminMixin):
    list_display = ['title', 'pages_used_on']


class LinkAdmin(JetCompactInline):
    model = Link
    extra = 0


@admin.register(LinkSet)
class LinkSetAdmin(VersionAdmin, UsedOnAdminMixin):
    list_display = ['__str__', 'pages_used_on']
    inlines = [LinkAdmin]


@admin.register(Sidebox)
class SideboxAdmin(VersionAdmin, UsedOnAdminMixin):
    list_display = ['__str__', 'pages_used_on']


class CardAdmin(LinkFieldsLastAdminMixin, JetCompactInline):
    model = Card
    extra = 0


@admin.register(CardSet)
class CardSetAdmin(VersionAdmin, UsedOnAdminMixin):
    list_display = ['__str__', 'pages_used_on']
    inlines = [CardAdmin]


class StatisticAdmin(LinkFieldsLastAdminMixin, JetCompactInline):
    model = Statistic
    extra = 0


@admin.register(StatSet)
class StatSetAdmin(VersionAdmin, UsedOnAdminMixin):
    list_display = ['__str__', 'pages_used_on']
    inlines = [StatisticAdmin]
