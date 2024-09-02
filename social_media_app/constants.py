LOGIN_SUCCESS_MESSAGE = "Login successfully."
USER_CREATED_SUCCESS_MESSAGE = "User created Successfully"
FRIEND_REQUETS_SUCCESS_MESSAGE = "Friend request send Successfully"
FRIEND_REQUETS_ACCEPETED_MESSAGE = "Friend request accepted Successfully"
FRIEND_REQUETS_REJECTED_MESSAGE = "Friend request rejected Successfully"

# error messages
DEFAULT_ERROR_MESSAGE = "Something went wrong. Please try again."
EMAIL_NOT_VALID_MESSAGE = "Invalid Email format."
EMAIL_ALREADY_EXIST_MESSAGE = "Email already exist."
EMAIL_ENTER_MESSAGE = "Please enter an email"
PASSWORD_ENTER_MESSAGE = "Please enter a password"
REQUESTCOUNT_EXCEEDED = "You have reached the max number of requests that can be send in a minute."
FRIEND_REQUEST_USER_ENTER_MESSAGE = "Please select a user"

# token messages
TOKEN_INVALID_MESSAGE = "Token invalid."
TOKEN_EXPIRED_MESSAGE = "Token expired."

ACCESS_TOKEN_EXPIRY_TIME = 60
__auth_tokens = None
REFRESH_TOKEN_EXPIRY_TIME = 365

PAGE_SIZE = 10

SKIP_URLS = [
    "/api/v1/user/login",
    "/api/v1/user/create"
]

FRIEND_REQUEST_ACCPTED_STATUS = 2
FRIEND_REQUEST_PENDING_STATUS = 1
FRIEND_REQUEST_REJECTED_STATUS = 3