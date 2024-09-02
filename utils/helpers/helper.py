from social_media_app import constants as const
from users.models import User
import logging

# helper to handle the error_message for response
def error_message(exception_name: str, exception):
    if (
        exception_name == "CustomValidation"
        or exception_name == "CustomException"
    ):
        message = str(exception)
    else:
        message = const.DEFAULT_ERROR_MESSAGE

    return message

def is_email_already_exist(email: str):
    try:
        print(email)
        if User.objects.filter(email=email) \
            .exclude(is_deleted=True) \
            .exists():
            return True
        return False
    except Exception as e:
        logging.getLogger("error_logger").error("Error in checking email exist or not")
        logging.getLogger("error_logger").error(str(e))