from django.core.paginator import Paginator
import logging
import re
from datetime import datetime
from social_media_app import constants as const

""" CLASS TO HANDLE UTILITY FUNCTIONS """


class Utils:
    # formatting validation errors
    @staticmethod
    def combine_validation_error(form_error: list, join: str="\n "):
        
        # initialize
        error_message = ""

        if form_error:
            if isinstance(form_error, list):
                for error in form_error:
                    if isinstance(error, dict):
                        for key, value in error.items():
                            if isinstance(value, list):
                                if error_message:
                                    error_message += join + join.join(value)
                                else:
                                    error_message += join.join(value)
                    else:
                        if error_message:
                            error_message += join + error
                        else:
                            error_message = error
            else:
                if isinstance(form_error, dict):
                    for key, value in form_error.items():
                        if isinstance(value, list):
                            if error_message:
                                error_message += join + join.join(value)
                            else:
                                error_message += join.join(value)

        return error_message

    # pagination functionality
    @staticmethod
    def pagination(
        queryset, page: int=1, limit: int=None):
        
        try:
            if not limit:
                limit = const.PAGE_SIZE

            if queryset:
                paginator = Paginator(
                    queryset, limit
                )  # calling django default pagination
                queryset = paginator.page(page)

        except Exception as e:
            queryset = []
            logging.getLogger("error_logger").error(
                "Pagination error: " + str(e)
            )

        response_data = {"queryset": queryset, "pagination": {}}
        return response_data

    @staticmethod
    def is_valid_email(email: str):
        # regular expression pattern for  email validation
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        regex = re.compile(pattern)

        # use the regex object to match the email address
        if regex.match(email):
            return True
        else:
            return False