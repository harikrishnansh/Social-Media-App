from rest_framework import serializers
from users.models import User
from social_media_app import constants as const
from utils.helpers.helper import is_email_already_exist

class UserLoginValidateSerializers(serializers.Serializer):
    def validate(self, data):
        error = {}
        user_data = None
        email = self.initial_data.get("email")
        password = self.initial_data.get("password")
        if email:
            if password:
                user =  User.objects.filter(email=email)
                user_data = user.last()
                if user_data:
                    user_password = user_data.password

                    # check for password is same
                    # if not check_password(password, user_password):
                    if not user_password == user_password:
                        error["password"] = ["Invalid credentials."]
                        
                else:
                    error["email"] = ["Invalid credentials."]
            else:
                error["password"] = ["Please enter the password."]
        else:
            error["email"] = ["Please enter the email."]
        if error:
            raise serializers.ValidationError(error)

        return data, user_data



class UserDataSerializers(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='id')
    name = serializers.CharField()
    email = serializers.CharField()
    dateOfBirth = serializers.CharField(source='dob')
    contactNumber = serializers.CharField(source='phone')

    class Meta:
        model = User
        fields = (
            "userId",
            "name",
            "email",
            "dateOfBirth",
            "contactNumber",
        )

    def __init__(self, *args, **kwargs):
        super(UserDataSerializers, self).__init__(*args, **kwargs)
        
        # connect to s3 bucket


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        email = data["email"]
        password = data["password"]
        if not email:                           
            raise serializers.ValidationError(const.EMAIL_ENTER_MESSAGE)
        if not password:                           
            raise serializers.ValidationError(const.PASSWORD_ENTER_MESSAGE)
        # check email already exist user
        if is_email_already_exist(email):                           
            raise serializers.ValidationError(const.EMAIL_ALREADY_EXIST_MESSAGE)
        
        return data