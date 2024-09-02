from rest_framework import permissions
from social_media_app import constants as const
from social_media_app.exceptions import CustomPermissionException
from friends.models import FriendRequest, Friends
from django.db.models import Q
from datetime import datetime
    
    
class FriendRequestCheckPermission(permissions.BasePermission):
    """
    Custom permission to allow only super admins.
    """

    def has_permission(self, request, view):
        login_user_id = request.payload.get("userId",None)
        recieving_user_id = request.data.get("userId",None)
        has_permission = True

        if not login_user_id or not recieving_user_id:
            has_permission = False
        
        #check whether sender and reciever are same
        if login_user_id == recieving_user_id:
            has_permission = False
        
        #Check if sender or reciver has already pending or accepted requests
        qq = Q()
        qq = qq &  Q(receiver=recieving_user_id)
        login_friend_request_data = FriendRequest.objects \
                .filter(status__in=[const.FRIEND_REQUEST_ACCPTED_STATUS,const.FRIEND_REQUEST_PENDING_STATUS])\
                .filter(qq)
        if login_friend_request_data.exists():
            has_permission = False

        if has_permission:
            return True
        raise CustomPermissionException()


class FriendRequestAcceptPermission(permissions.BasePermission):
    """
    Custom permission to allow only super admins.
    """

    def has_permission(self, request, view):
        login_user_id = request.payload.get("userId",None)
        request_send_user_id = request.data.get("sendUserId",None)
        has_permission = True

        if not login_user_id or not request_send_user_id:
            has_permission = False
        
        #check whether sender and reciever are same
        if login_user_id == request_send_user_id:
            has_permission = False
        
        #Check if reciver has already accepted request from sending user
        accepting_user_data = FriendRequest.objects \
                .filter(status=const.FRIEND_REQUEST_ACCPTED_STATUS,receiver=login_user_id,sender=request_send_user_id)
        if accepting_user_data.exists():
            has_permission = False
        
        #Check if there is pending user data from sender
        pending_user_data = FriendRequest.objects \
                .filter(status=const.FRIEND_REQUEST_PENDING_STATUS,receiver=login_user_id,sender=request_send_user_id)
        if not pending_user_data.exists():
            has_permission = False

        if has_permission:
            return True
        raise CustomPermissionException()


class FriendRequestRejectPermission(permissions.BasePermission):
    """
    Custom permission to allow only super admins.
    """

    def has_permission(self, request, view):
        login_user_id = request.payload.get("userId",None)
        request_send_user_id = request.data.get("sendUserId",None)
        has_permission = True

        if not login_user_id or not request_send_user_id:
            has_permission = False
        
        #check whether sender and reciever are same
        if login_user_id == request_send_user_id:
            has_permission = False
        
        #Check if reciver has already accepted request from sending user
        rejecting_user_data = FriendRequest.objects \
                .filter(status=const.FRIEND_REQUEST_REJECTED_STATUS,receiver=login_user_id,sender=request_send_user_id)
        if rejecting_user_data.exists():
            has_permission = False
        
        #Check if there is pending user data from sender
        pending_user_data = FriendRequest.objects \
                .filter(status=const.FRIEND_REQUEST_PENDING_STATUS,receiver=login_user_id,sender=request_send_user_id)
        if not pending_user_data.exists():
            has_permission = False

        if has_permission:
            return True
        raise CustomPermissionException()
