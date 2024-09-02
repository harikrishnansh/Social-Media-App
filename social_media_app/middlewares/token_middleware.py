import jwt
from social_media_app import settings, constants as const
import logging
from django.http import JsonResponse
from rest_framework import status
from datetime import datetime



""" AUTHENTICATION MIDDLEWARE """


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *view_kwargs):
        path = request.META["PATH_INFO"]

        # Initialize Payload
        request.payload = {}
        # skip urls from checking token
        if path in const.SKIP_URLS or request.path.startswith(settings.MEDIA_URL):
            pass  # do nothing
        else:
            # get the token from request_header 
            header_token = request.META.get("HTTP_X_AUTHORIZATION", None)
            try:
                # if header_token is not None decode payload from token, otherwise return error
                if header_token: 
                    # replace word 'Token' from the string
                    token = header_token.replace("Token ", "")

                    # decode token to fetch user/admin details
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                                         "HS256"], options={"verify_signature": True})
                    
                    # if payload is available proceed for authentication checks, else return error 
                    if payload:
                        # check for token validity
                        expiry_date = payload.get("expiry", None)
                        if expiry_date:
                            now = datetime.utcnow()

                            # convert string to date time
                            expiry_on = datetime.strptime(
                                expiry_date, "%Y-%m-%d %H:%M:%S")

                            # token expired
                            if expiry_on < now:
                                return JsonResponse(
                                    {
                                        "hasError": True,
                                        "errorCode": 1001,
                                        "message": const.TOKEN_EXPIRED_MESSAGE,
                                        "debugMessage": "",
                                        "response": {},
                                    },
                                    status=status.HTTP_401_UNAUTHORIZED,
                                )
                            else:
                                request.payload = payload  # send payload to request data
                        else:
                            return JsonResponse(
                                {
                                    "hasError": True,
                                    "errorCode": 1001,
                                    "message": const.TOKEN_INVALID_MESSAGE,
                                    "debugMessage": "Expiry flag missing or null",
                                    "response": {},
                                },
                                status=status.HTTP_401_UNAUTHORIZED,
                            )
                    else:
                        return JsonResponse(
                            {
                                "hasError": True,
                                "errorCode": 1001,
                                "message": const.TOKEN_INVALID_MESSAGE,
                                "debugMessage": "Payload not found after decoding jwt",
                                "response": {},
                            },
                            status=status.HTTP_401_UNAUTHORIZED,
                        )
                else:
                    return JsonResponse(
                        {
                            "hasError": True,
                            "errorCode": 410,
                            "message": const.TOKEN_INVALID_MESSAGE,
                            "debugMessage": "Token missing on the header",
                            "response": {},
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

            except Exception as e:
                logging.getLogger("error_logger").error(
                    "Token middleware Error:")
                logging.getLogger("error_logger").error(str(e))

                return JsonResponse(
                    {
                        "hasError": True,
                        "errorCode": 1001,
                        "message": const.DEFAULT_ERROR_MESSAGE,
                        "debugMessage": str(e),
                        "response": {},
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

