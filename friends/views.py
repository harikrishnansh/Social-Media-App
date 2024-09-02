from social_media_app import constants as const
from social_media_app.exceptions import CustomException, CustomValidation
from rest_framework.response import Response
from social_media_app.response import error_, success_
from friends.serialisers import (FriendRequestSerialiser, FriendsSerialiser,PendingRequestSerialiser)
from rest_framework.views import APIView
import json
from rest_framework import status
from utils.utils import Utils
from utils.helpers.helper import error_message
from .models import FriendRequest, Friends
from datetime import datetime, timedelta
from social_media_app.permissions import (FriendRequestCheckPermission,
                                          FriendRequestAcceptPermission,
                                          FriendRequestRejectPermission)
from users.models import User
from django.db.models import Q

# Create your views here.

class SendFriendRequest(APIView):

    permission_classes = [FriendRequestCheckPermission]

    def post(self, request):
        try:
            payload = request.payload
            login_user_id = request.payload.get("userId",None)
            recieving_user_id = request.data.get("userId",None)

            #Check if sender has more than 3 friend requests in past 1 minute
            current_date_time = datetime.now()
            date_time_one_min_ago = current_date_time - timedelta(minutes=1)
            sender_friend_request_data = FriendRequest.objects.\
                            filter(sender=login_user_id,status=const.FRIEND_REQUEST_PENDING_STATUS,created_at__gt=date_time_one_min_ago)
            count = sender_friend_request_data.count()
            if count > 3:
                raise CustomValidation(const.REQUESTCOUNT_EXCEEDED)
    
            validate_data = {
                "sender": login_user_id,
                "receiver": recieving_user_id
            }

            serializer = FriendRequestSerialiser(
                data=validate_data
            )  # calling serializer
            if not serializer.is_valid():  # not a valid form
                errors = json.loads(json.dumps(serializer.errors))

                # combine errors to form a single word
                errors_data = Utils.combine_validation_error(errors)
                raise CustomException(errors_data)
            else:
                serializer.save()
                for data in FriendRequest.objects.all():
                    print(data.sender.id,data.receiver.id)
                response_data = {}
                return Response(
                    success_(
                        message=const.FRIEND_REQUETS_SUCCESS_MESSAGE,
                        response=response_data,
                    ),
                    status=status.HTTP_200_OK,
                )
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


class AcceptFriendRequest(APIView):

    permission_classes = [FriendRequestAcceptPermission]

    def post(self, request):
        try:
            login_user_id = request.payload.get("userId",None)
            request_send_user_id = request.data.get("sendUserId",None)
            
            friend_request_data = FriendRequest.objects.\
                        filter(status=const.FRIEND_REQUEST_PENDING_STATUS,
                        sender=request_send_user_id,receiver=login_user_id).last()
            
            friend_request_data.status=const.FRIEND_REQUEST_ACCPTED_STATUS
            friend_request_data.save()

            friends = Friends()
            friends.sender = User.objects.filter(id=request_send_user_id).last()
            friends.receiver = User.objects.filter(id=login_user_id).last()
            friends.save()
    
            return Response(
                    success_(
                        message=const.FRIEND_REQUETS_ACCEPETED_MESSAGE,
                        response={},
                    ),
                    status=status.HTTP_200_OK,
                )
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

class RejectFriendRequest(APIView):

    permission_classes = [FriendRequestRejectPermission]

    def post(self, request):
        try:
            login_user_id = request.payload.get("userId",None)
            request_send_user_id = request.data.get("sendUserId",None)
            
            friend_request_data = FriendRequest.objects.\
                        filter(status=const.FRIEND_REQUEST_PENDING_STATUS,
                        sender=request_send_user_id,receiver=login_user_id).last()
            
            friend_request_data.status=const.FRIEND_REQUEST_REJECTED_STATUS
            friend_request_data.save()
    
            return Response(
                    success_(
                        message=const.FRIEND_REQUETS_REJECTED_MESSAGE,
                        response={},
                    ),
                    status=status.HTTP_200_OK,
                )
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


class FriendsList(APIView):


    def post(self, request):
        try:
            login_user_id = request.payload.get("userId",None)
            search_key = request.payload.get("searchKey","")

            qq = Q()
            if search_key:
                qq = qq &  Q(sender__name__icontains=search_key)
            friend_request_data = Friends.objects.\
                        filter(receiver=login_user_id).select_related("sender").filter(qq)
            
            serialiser = FriendsSerialiser(friend_request_data,many=True)
            
            response = {
                "allFriends" : serialiser.data
            }
    
            return Response(
                    success_(
                        message="Success",
                        response=response,
                    ),
                    status=status.HTTP_200_OK,
                )
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


class PendingRequests(APIView):

    def post(self, request):
        try:
            login_user_id = request.payload.get("userId",None)
            search_key = request.payload.get("searchKey","")
            
            if search_key:
                qq = qq &  Q(sender__name__icontains=search_key)
            friend_request_data = FriendRequest.objects.\
                        filter(receiver=login_user_id,status = const.FRIEND_REQUEST_PENDING_STATUS)\
                            .select_related("sender").filter(qq)
            
            serialiser = PendingRequestSerialiser(friend_request_data,many=True)
            
            response = {
                "pendingRequests" : serialiser.data
            }
    
            return Response(
                    success_(
                        message="Success",
                        response=response,
                    ),
                    status=status.HTTP_200_OK,
                )
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