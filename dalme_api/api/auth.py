from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.response import Response
from rest_framework.views import APIView

from dalme_api.serializers.users import UserSerializer


class Auth(APIView):
    """API for JSON, refresh auth via ajax, supplemental to DalmeLogin."""
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def create_session(request, user):
        """Adapted from the Django login method.
        https://github.com/django/django/blob/7cca22964c09e8dafc313a400c428242404d527a/django/contrib/auth/__init__.py#L90
        """
        request.session.clear()
        request.session.cycle_key()
        request.session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)
        request.session[auth.BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
        request.session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
        request.session.save()

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        """Login with JSON payload."""
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                serialized = UserSerializer(user, fields=['username', 'id'])
                response = Response(serialized.data, 200)
                self.create_session(request, user)
                response.set_cookie('sessionid', request.session.session_key)
                return response
        return Response({'error': 'Unauthorized'}, 401)
