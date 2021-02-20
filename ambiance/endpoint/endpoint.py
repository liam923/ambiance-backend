from json import JSONDecodeError
from typing import Callable, Any

from django.http import HttpRequest, JsonResponse, Http404, HttpResponse

GET = "GET"
POST = "POST"
PUT = "PUT"


def endpoint(
    params: Any = None, body: Any = None, method: str = GET
) -> Callable[[Callable], Callable[[HttpRequest], HttpResponse]]:
    def endpoint_callback(
        endpoint_function: Callable,
    ) -> Callable[[HttpRequest], HttpResponse]:
        def inner(request: HttpRequest) -> HttpResponse:
            print(request.method)
            if request.method == method:
                if body is not None:
                    try:
                        decoded_body = body.from_json(request.body)
                    except (JSONDecodeError, KeyError):
                        return JsonResponse(
                            {"message": "Invalid JSON schema"}, status=400
                        )
                else:
                    decoded_body = None

                if params is not None:
                    try:
                        params_dict = {
                            key: val[0] for key, val in dict(request.GET).items()
                        }
                        decoded_url_params = params.from_dict(params_dict)
                    except (JSONDecodeError, KeyError):
                        return JsonResponse({"message": "Invalid params"}, status=400)
                else:
                    decoded_url_params = None

                result = endpoint_function(
                    params=decoded_url_params, body=decoded_body, user="USER_ID"
                ).to_dict()
                return JsonResponse(result)
            else:
                raise Http404()

        return inner

    return endpoint_callback
