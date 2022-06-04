from drf_yasg import openapi


def get_phone_number():
    phone_number = openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number",
                                     type=openapi.TYPE_STRING)

    action = openapi.Parameter('type', openapi.IN_QUERY, description="To register a user, type client in the type",
                               type=openapi.TYPE_STRING)

    return [phone_number, action]


def get_user_phone_and_code():
    phone_number = openapi.Parameter('phone', openapi.IN_QUERY, description='Phone number',
                                     type=openapi.TYPE_STRING)
    verify_code = openapi.Parameter('code', openapi.IN_QUERY, description='Verification code',
                                    type=openapi.TYPE_STRING)
    return [phone_number, verify_code]