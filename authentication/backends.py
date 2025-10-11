from rest_framework.authentication import get_authorization_header


from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.conf import settings
import jwt


from rest_framework import exceptions

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_data = get_authorization_header(request)
        if not auth_data:
            return None
        # Assume the token is in the format "Bearer <token>" this decodes the token
        try:
            # Split the token and get the actual token part
            _, token = auth_data.decode('utf-8').split(' ')
            # Decode the token to get the payload
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            # Get the user from the payload
            user = User.objects.get(username=payload['username'])
            # Optionally, you can attach the token to the user object
            user.auth_token = token
            return (user, token)
        # Handle exceptions
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found, login again')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Your token is invalid, login again')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Your token is expired, login again')

        # Optionally, you can remove this line as it is unreachable
        # return super().authenticate(request)

   