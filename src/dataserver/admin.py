from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . import models


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'organisation_name',)
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def organisation_name(self, obj):  # pylint: disable=no-self-use
        link = reverse('admin:dataserver_organisation_change', args=(
            obj.organisation.id,))
        return format_html(
            '<a href="%s">%s</a>' % (link, obj.organisation.name))
    organisation_name.short_description = 'Organisation'
    organisation_name.admin_order_field = 'organisation__name'


class OrganisationDeviceAdmin(admin.StackedInline):
    model = models.Device
    can_delete = False
    extra = 0
    fieldsets = ((None, {"fields": (),}),)

    def has_add_permission(self, request, obj):
        return False


class OrganisationApiKeyAdmin(admin.StackedInline):
    model = models.ApiKey
    extra = 0


class OrganisationAdmin(admin.ModelAdmin):
    inlines = [OrganisationDeviceAdmin, OrganisationApiKeyAdmin]
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.Organisation, OrganisationAdmin)
