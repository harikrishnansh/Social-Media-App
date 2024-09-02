def success_(message: str="success", response: dict={}):
    res_array = {
        "hasError": False,
        "errorCode": -1,
        "message": message,
        "response": response,
    }
    return res_array


# returns error response
def error_(
    request=None,
    message: str="failed",
    error_code: int=1001,
    debug_message: str="",
    response: dict=None,
    failure_response: dict={},
):

    res_array = {
        "hasError": True,
        "errorCode": error_code,
        "message": message,
        "debugMessage": debug_message,
        "response": response,
        "failureResponse": failure_response,
    }
    return res_array
