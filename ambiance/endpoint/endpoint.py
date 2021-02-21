from json import JSONDecodeError
from typing import Callable, Any

from django.http import HttpRequest, JsonResponse, Http404, HttpResponse

from ambiance.auth import token
from ambiance.model.error import Error, ErrorMessage

GET = "GET"
POST = "POST"
PUT = "PUT"


def endpoint(
    params: Any = None,
    body: Any = None,
    header: Any = None,
    method: str = GET,
    auth_required: bool = True,
    unencoded_return: bool = True,
) -> Callable[[Callable], Callable[[HttpRequest], HttpResponse]]:
    def endpoint_callback(
        endpoint_function: Callable,
    ) -> Callable[[HttpRequest], HttpResponse]:
        def inner(request: HttpRequest) -> HttpResponse:
            if request.method == method:
                if body is not None:
                    try:
                        decoded_body = body.from_json(request.body)
                    except (JSONDecodeError, KeyError):
                        return Error(
                            status_code=400, message=ErrorMessage("Invalid JSON schema")
                        ).as_response()
                else:
                    decoded_body = None

                if params is not None:
                    try:
                        params_dict = {
                            key: val[0] for key, val in dict(request.GET).items()
                        }
                        decoded_url_params = params.from_dict(params_dict)
                    except (JSONDecodeError, KeyError):
                        return Error(
                            status_code=400, message=ErrorMessage("Invalid params")
                        ).as_response()
                else:
                    decoded_url_params = None

                if header is not None:
                    try:
                        header_dict = {
                            key: val for key, val in dict(request.headers).items()
                        }
                        decoded_header = params.from_dict(header_dict)
                    except (JSONDecodeError, KeyError):
                        return Error(
                            status_code=400, message=ErrorMessage("Invalid header")
                        ).as_response()
                else:
                    decoded_header = None

                user_id = None
                if "User-Token" in request.headers:
                    user_id = token.verify(request.headers["User-Token"])

                if user_id is None and auth_required:
                    return Error(status_code=401).as_response()

                try:
                    result = endpoint_function(
                        params=decoded_url_params,
                        body=decoded_body,
                        header=decoded_header,
                        user=user_id,
                        request_uri=request.get_raw_uri(),
                    )

                    if unencoded_return:
                        return JsonResponse(result.to_dict())
                    else:
                        return result
                except Error as error:
                    return error.as_response()
            else:
                raise Http404()

        return inner

    return endpoint_callback
