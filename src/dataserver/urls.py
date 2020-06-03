from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import Http404
from django.urls import re_path
from django.views.defaults import page_not_found
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    re_path('^api/v2[^/]*/upload/?$', views.upload_view),
    re_path(
        '^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('images/favicon.ico'),
            permanent=False),
        name="favicon"),
    re_path(
        '.*',
        page_not_found,
        {'exception': Http404()}),
]
