from rest_framework import serializers
from friends.models import FriendRequest, Friends
from social_media_app import constants as const
from users.models import User

class FriendRequestSerialiser(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"
    
    def validate(self, data):
        receiver = self.initial_data.get("receiver",None)
        if not receiver:                           
            raise serializers.ValidationError(const.FRIEND_REQUEST_USER_ENTER_MESSAGE)
        if not User.objects.filter(id=receiver).exists():                           
            raise serializers.ValidationError(const.FRIEND_REQUEST_USER_ENTER_MESSAGE)
        
        return data


class FriendsSerialiser(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()

    class Meta:
        model = Friends
        fields = ["name","email","phone","dob"]
    
    def get_name(self, obj):
        return obj.sender.name

    def get_email(self, obj):
        return obj.sender.email
    
    def get_phone(self, obj):
        return obj.sender.phone
    
    def get_dob(self, obj):
        return obj.sender.dob


class PendingRequestSerialiser(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ["name","email","phone","dob"]
    
    def get_name(self, obj):
        return obj.sender.name

    def get_email(self, obj):
        return obj.sender.email
    
    def get_phone(self, obj):
        return obj.sender.phone
    
    def get_dob(self, obj):
        return obj.sender.dob