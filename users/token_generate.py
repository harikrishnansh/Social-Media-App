import jwt
import secrets
from datetime import datetime, timedelta
from social_media_app import settings, constants as const
import logging
from users.models import User

# Generate AuthenticationToken for user
class UserAuthToken:
    __auth_tokens = None
    __refresh_token = None

    def __init__(self):

        expiry_value = const.ACCESS_TOKEN_EXPIRY_TIME
        refresh_expiry_value = const.REFRESH_TOKEN_EXPIRY_TIME
        self.token_expiry = expiry_value 
        self.refresh_token_expiry = refresh_expiry_value 

    def generate(self, user: User):
        try:
            now = datetime.utcnow() # fetch current time
            expiry = now + timedelta(days=int(self.token_expiry))
            expiry_on = expiry.strftime("%Y-%m-%d %H:%M:%S")

            refresh_expiry = now + timedelta(days=int(self.refresh_token_expiry)) # set refresh token_expiry
            refresh_expiry_on = refresh_expiry.strftime("%Y-%m-%d %H:%M:%S")
            
            secret_token = secrets.token_hex(8) # create a random token
            secret_refresh_token = secrets.token_hex(10) # create a random token

            access_obj = {
                "userId": user.id, 
                "secretToken": secret_token,
                "expiry": expiry_on,
            }

            refresh_obj = {
                "userId": user.id, 
                "secretRefreshToken": secret_refresh_token,
                "expiry": refresh_expiry_on,
            }
            
            # store access_token and refresh_token to db
            self.__auth_tokens = jwt.encode(access_obj, settings.SECRET_KEY, algorithm="HS256")

            self.__refresh_token = jwt.encode(refresh_obj, settings.SECRET_KEY, algorithm="HS256")

            return {
                "accessToken": self.__auth_tokens,
                "refreshToken": self.__refresh_token,
                "tokenExpiryTime": int(datetime.timestamp(expiry) * 1000)
            }

        except Exception as e:
            logging.getLogger("error_logger").error("Creating tokens failed:")
            logging.getLogger("error_logger").error(str(e))
            return {
                "accessToken": None,
                "refreshToken": None,
                "tokenExpiryTime": None
            }