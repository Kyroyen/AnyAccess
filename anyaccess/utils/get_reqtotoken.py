from rest_framework.exceptions import AuthenticationFailed

def request_to_auth_token(request):
    auth = request.META.get('HTTP_AUTHORIZATION').split()
    # print(auth)

    if len(auth) == 1:
        msg = ('Invalid token header. No credentials provided.')
        raise AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = ('Invalid token header. Token string should not contain spaces.')
        raise AuthenticationFailed(msg)
    
    return auth