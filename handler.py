from django.conf.urls import url
from django.http import HttpRequest, JsonResponse

DEBUG = True
SECRET_KEY = "peepeepoopoojizzjazz"
ROOT_URLCONF = __name__


def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "Hello world."})


urlpatterns = [url(r"^$", home)]
