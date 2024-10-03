import os
import requests
import jwt
from dataclasses import dataclass
from random import SystemRandom
from urllib.parse import urlencode
from urllib.parse import urljoin

from .forms import NewUserForm
from .models import Profile

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.urls import reverse_lazy


UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

# GOOGLE OAUTH2 REGISTRATION/LOGIN

def Login(request):
    return render(request, "login.html")

@dataclass
class GoogleRawLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


class GoogleOAuthView(View):
    def get(self, request, *args, **kwargs):

        google_login_flow = GoogleRawLoginFlowService()

        if request.GET.get('code'):

            user = google_login_flow.finalize_auth(request)
            
            login(request, user)
            return redirect("/dashboard")

        else: 
            authorization_url, state = google_login_flow.get_authorization_url()

            request.session["google_oauth2_state"] = state

            return redirect(authorization_url)


class GoogleRawLoginFlowService:
    API_URI = reverse_lazy("users:register_google")

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]

    def __init__(self):
        self._credentials = self._google_raw_login_get_credentials()


    def _google_raw_login_get_credentials(self) -> GoogleRawLoginCredentials:
        client_id = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET")
        project_id = os.environ.get("GOOGLE_OAUTH2_PROJECT_ID")

        if not client_id:
            raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env.")

        if not client_secret:
            raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_SECRET missing in env.")

        if not project_id:
            raise ImproperlyConfigured("GOOGLE_OAUTH2_PROJECT_ID missing in env.")

        credentials = GoogleRawLoginCredentials(
            client_id=client_id,
            client_secret=client_secret,
            project_id=project_id
        )

        return credentials

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        domain = settings.BASE_BACKEND_URL
        api_uri = str(self.API_URI)
        redirect_uri = urljoin(domain, api_uri)
        return redirect_uri

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state

    def finalize_auth(self, request) -> User:
        code = request.GET.get('code')
        error = request.GET.get('error')
        state = request.GET.get('state')

        if state != request.session["google_oauth2_state"]:
            raise ImproperlyConfigured("The session cookies do not match!")
        if error is not None:
            raise Exception(error)

        client_id = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET")
        redirect_uri = self._get_redirect_uri()
        grant_type = 'authorization_code'

        post_data = {
            "code": code,
            "client_id": client_id, 
            "client_secret": client_secret, 
            "redirect_uri": redirect_uri, 
            "grant_type": grant_type
        }

        try:
            response = requests.post('https://oauth2.googleapis.com/token', data=post_data)
            data = response.json()
            id_token = data['id_token']
        except Exception as e:
            return redirect("/dashboard")
        decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
        email = decoded_token['email']
        # TODO: How is this best used?  
        # email_verified = decoded_token['email_verified']
        first_name = decoded_token['given_name']
        family_name = decoded_token['family_name']

        try:
            user = User.objects.get(email=email)
        
        except ObjectDoesNotExist as e:
            user = User.objects.create(username=email, email=email, first_name=first_name, last_name=family_name )
            user.save()

        return user