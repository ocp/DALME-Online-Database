"""Resources and endpoints for OAuth 2.0 spec authentication.

Other than the OAuth Application model that is defined alongside the other
models in this layer, this module represents a full OAuth 2.0 flow with the
PKCE extension.

"""

import json

from oauth2_provider import urls as oauth2_urls
from oauth2_provider import views as oauth2_views
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.views import TokenView
from rest_framework import permissions, serializers, status, views
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.urls import re_path

from api.access_policies import BaseAccessPolicy
from api.resources.groups import GroupSerializer

from .context import get_current_tenant


class AuthAccessPolicy(BaseAccessPolicy):
    """Access policies for authorization and authentication."""

    id = 'auth-policy'


class LoginSerializer(serializers.Serializer):
    """Serializer for session login."""

    username = serializers.CharField(label='username', write_only=True)
    password = serializers.CharField(
        label='password', style={'input_type': 'password'}, trim_whitespace=True, write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = 'Access denied: incorrect username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required fields.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class AuthorizationCode(views.APIView):
    """API endpoint that receives the OIDC authorization token."""

    def get(self, request):  # noqa: ARG002
        return Response(None, status=status.HTTP_200_OK)


class Login(views.APIView):
    """API endpoint for session authentication login."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):  # noqa: A002, ARG002
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        return Response(None, status=status.HTTP_202_ACCEPTED)


class IDAOAuth2Validator(OAuth2Validator):
    """Override the built-in OAuth claims response."""

    def get_userinfo_claims(self, request):
        """Enhance the default OIDC claims payload."""
        claims = super().get_userinfo_claims(request)
        avatar = request.user.avatar_url
        tenant = get_current_tenant()

        claims.update(
            {
                'avatar': avatar,
                'email': request.user.email,
                'username': request.user.username,
                'full_name': request.user.full_name,
                'is_admin': request.user.is_staff,
                'groups': GroupSerializer(request.user.groups_scoped, many=True).data,
                'tenant': {
                    'id': tenant.pk,
                    'name': tenant.name,
                },
            }
        )

        return claims


class OAuthToken(TokenView):
    """Override the django-oauth-toolkit token view.

    This allows us to return the refresh token in a HTTP only cookie instead of
    the response body, making things more secure against potential
    vulenerabilities.

    """

    permission_classes = [AuthAccessPolicy]

    def post(self, request, *args, **kwargs):
        """Generate the OAuth token response payload.

        We want the refresh token to be stored in a cookie not returned in the
        body along with the other data so we need to deserialize the payload,
        pop the token, set the cookie and reserialize the data before the
        return. Likewise, if we are requesting a new new access token with a
        refresh token (ie. when grant type is 'refresh_token') make sure to
        read the token data from the cookie.

        """
        data = request.POST.copy()
        data['client_secret'] = settings.OAUTH_CLIENT_SECRET
        if data['grant_type'] == 'refresh_token':
            refresh_token = request.COOKIES.get('refresh_token')
            data['refresh_token'] = refresh_token
        request.POST = data

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            data = json.loads(response.content.decode('utf-8'))
            refresh_token = data.pop('refresh_token')
            response.content = json.dumps(data).encode('utf-8')

            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=settings.OAUTH2_REFRESH_TOKEN_COOKIE_EXPIRY,
                httponly=True,
                samesite='Lax',
                secure=not settings.IS_DEV,
            )

        return response


urls = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name='authorize'),
    re_path(r'^authorize/callback/$', AuthorizationCode.as_view(), name='authorization-code'),
    re_path(r'^login/$', Login.as_view(), name='login'),
    re_path(r'^token/$', OAuthToken.as_view(), name='token'),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name='revoke-token'),
    re_path(r'^introspect/$', oauth2_views.IntrospectTokenView.as_view(), name='introspect'),
    *oauth2_urls.management_urlpatterns + oauth2_urls.oidc_urlpatterns,
]
