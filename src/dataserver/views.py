from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import logfiles, models


class UploadV1View(View):

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        if len(request.GET.getlist('api_key')) != 1:
            return HttpResponseForbidden()
        try:
            api_key = models.ApiKey.objects.get(
                key__exact=request.GET['api_key'])
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return HttpResponseForbidden()
        logfiles.decode_and_save(request.body, api_key.organisation)
        return HttpResponse()


upload_v1_view = csrf_exempt(UploadV1View.as_view())
