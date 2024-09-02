from social_media_app import constants as const
from social_media_app.exceptions import CustomException, CustomValidation
from rest_framework.response import Response
from social_media_app.response import error_, success_
from users.serialisers import (UserLoginValidateSerializers, UserDataSerializers,
                               CreateUserSerializer)
from users.token_generate import UserAuthToken
from rest_framework.views import APIView
import json
from rest_framework import status
from utils.utils import Utils
from utils.helpers.helper import error_message
from datetime import datetime


# Create your views here.
class UserLogin(APIView):

    def post(self, request):
        try:
            request_data = request.data
            validate_data = {
                "email": request_data.get("email",None),
                "password": request_data.get("password",None),
            }

            # validate data using serializer
            serializer = UserLoginValidateSerializers(
                data=validate_data
            )
            if serializer.is_valid():
                _, user_obj = serializer.validated_data
                user_serializer = UserDataSerializers(
                    user_obj, many=False,
                )
                user_token = UserAuthToken().generate(
                                user_obj
                            )
                message = const.LOGIN_SUCCESS_MESSAGE

                response_data = {
                    "user": user_serializer.data,
                    "auth": user_token,
                    "statusMessage": message
                }
                                
                return Response(
                    success_(
                        message=message, response=response_data
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                errors = json.loads(json.dumps(serializer.errors))
                # combine errors to form a single word.
                errors_data = Utils.combine_validation_error(errors)
                raise CustomValidation(errors_data)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response(
                error_(
                    request=request,
                    message=error_message(e.__class__.__name__, e),
                    debug_message=str(e),
                ),
                status=status.HTTP_200_OK,
            )


class UserCreation(APIView):

    def post(self, request):
        try:
            # initialize payload
            request_data = request.data

            # email validation.
            if not Utils.is_valid_email(
                request_data.get("email", None)
            ):
                raise CustomValidation(const.EMAIL_NOT_VALID_MESSAGE)

            validate_data = {
                "name": request_data.get("name", None),
                "email": request_data.get("email", None).lower(),
                "phone": request_data.get("contactNumber", None),
                "dob": request_data.get("dob", ""),  # YY-MM-DD
                "created_at": datetime.utcnow(),
                "password" : request_data.get("password", "")
            }

            # create new user
            serializer = CreateUserSerializer(
                data=validate_data
            )  # calling serializer
            if not serializer.is_valid():  # not a valid form
                errors = json.loads(json.dumps(serializer.errors))

                # combine errors to form a single word
                errors_data = Utils.combine_validation_error(errors)
                raise CustomException(errors_data)
            else:
                saved_data = serializer.save()
                user_id = saved_data._get_pk_val()
                response_data = {"user": {"userId": user_id}}
                return Response(
                    success_(
                        message=const.USER_CREATED_SUCCESS_MESSAGE,
                        response=response_data,
                    ),
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                error_(
                    request=request,
                    message=error_message(e.__class__.__name__, e),
                    debug_message=str(e),
                ),
                status=status.HTTP_200_OK,
            )