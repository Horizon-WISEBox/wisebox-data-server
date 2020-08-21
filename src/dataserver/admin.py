from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import Truncator

from . import models


class DeviceAdmin(admin.ModelAdmin):

    exclude = ('organisation',)

    list_display = ('obj_id', 'mac', 'device_short_notes', 'organisation_link',)

    list_display_links = ('obj_id', 'mac',)

    readonly_fields = ('mac', 'organisation_link',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def obj_id(self, obj): # pylint: disable=no-self-use
        return format_html(str(obj))
    obj_id.short_description = 'ID'

    def organisation_link(self, obj): # pylint: disable=no-self-use
        link = reverse('admin:dataserver_organisation_change', args=(
            obj.organisation.id,))
        return format_html(
            '<a href="%s">%s</a>' % (link, str(obj.organisation)))
    organisation_link.short_description = 'Organisation'
    organisation_link.admin_order_field = 'organisation__name'

    def device_short_notes(self, obj): # pylint: disable=no-self-use
        truncator = Truncator(obj.notes)
        return format_html(truncator.chars(50, truncate='...'))
    device_short_notes.short_description = 'Notes'


class OrganisationDeviceAdmin(admin.StackedInline):
    model = models.Device
    can_delete = False
    extra = 0
    fieldsets = ((None, {"fields": (),}),)
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


class OrganisationApiKeyAdmin(admin.StackedInline):
    model = models.ApiKey
    extra = 0


class OrganisationAdmin(admin.ModelAdmin):

    inlines = [OrganisationDeviceAdmin, OrganisationApiKeyAdmin]

    list_display = ('obj_id', 'name',)

    list_display_links = ('obj_id', 'name',)

    def obj_id(self, obj): # pylint: disable=no-self-use
        return format_html(str(obj))
    obj_id.short_description = 'ID'


class LocationAdmin(admin.ModelAdmin):

    list_display = ('obj_id', 'name', 'organisation_link',)

    list_display_links = ('obj_id', 'name',)

    def obj_id(self, obj): # pylint: disable=no-self-use
        return format_html(str(obj))
    obj_id.short_description = 'ID'

    def get_exclude(self, request, obj=None):
        if obj:
            return ('organisation',)
        return ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('name', 'organisation_link',)
        return ()

    def organisation_link(self, obj): # pylint: disable=no-self-use
        link = reverse('admin:dataserver_organisation_change', args=(
            obj.organisation.id,))
        return format_html(
            '<a href="%s">%s</a>' % (link, str(obj.organisation)))
    organisation_link.short_description = 'Organisation'
    organisation_link.admin_order_field = 'organisation__name'


class DeviceSessionAdmin(admin.ModelAdmin):

    list_display = (
        'obj_id', 'start_date', 'end_date', 'device_link', 'location_link',)

    def get_exclude(self, request, obj=None):
        if obj:
            return ('device', 'location',)
        return ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('device_link', 'location_link',)
        return ()

    def obj_id(self, obj): # pylint: disable=no-self-use
        return format_html(str(obj))
    obj_id.short_description = 'ID'

    def device_link(self, obj): # pylint: disable=no-self-use
        link = reverse('admin:dataserver_device_change', args=(
            obj.device.id,))
        return format_html(
            '<a href="%s">%s</a>' % (link, str(obj.device)))
    device_link.short_description = 'Device'
    device_link.admin_order_field = 'device__mac'

    def location_link(self, obj): # pylint: disable=no-self-use
        link = reverse('admin:dataserver_location_change', args=(
            obj.location.id,))
        return format_html(
            '<a href="%s">%s</a>' % (link, str(obj.location)))
    location_link.short_description = 'Location'
    location_link.admin_order_field = 'location__name'


admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.Organisation, OrganisationAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.DeviceSession, DeviceSessionAdmin)
