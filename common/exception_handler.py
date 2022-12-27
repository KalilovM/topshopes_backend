from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler
    return {status_code, message, errors}
    """

    response = exception_handler(exc, context)

    if response is not None:
        print(response)
        print("Response data")
        print(response.data)

    print(exc, context)

    return response
