import os
import requests
import jwt
from dataclasses import dataclass
from random import SystemRandom
from urllib.parse import urlencode

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

# DJANGO BUILT-IN REGISTRATION
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("/dashboard")

    form = NewUserForm()
    context = {"form": form}

    return render(request, "register.html", context)

# GOOGLE OAUTH2 REGISTRATION/LOGIN

@dataclass
class GoogleRawLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


class GoogleOAuthView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('code'):

            code = request.GET.get('code')
            error = request.GET.get('error')
            state = request.GET.get('state')

            if state != request.session["google_oauth2_state"]:
                raise ImproperlyConfigured("The session cookies do not match!")
            if error is not None:
                raise Exception(error)

            client_id = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID")
            client_secret = os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET")
            redirect_uri = 'http://localhost:8000/users/register_google'
            grant_type = 'authorization_code'

            post_data = {
                "code": code,
                "client_id": client_id, 
                "client_secret": client_secret, 
                "redirect_uri": redirect_uri, 
                "grant_type": grant_type
            }

            response = requests.post('https://oauth2.googleapis.com/token', data=post_data)
            data = response.json()
            id_token = data['id_token']
            decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
            email = decoded_token['email']
            email_verified = decoded_token['email_verified']

            # if email_verified:
            try:
                user = User.objects.get(email=email)
            
            except ObjectDoesNotExist as e:
                user = User.objects.create(username=email, email=email)
                user.save()
            
            login(request, user)
            return redirect("/dashboard")

        else: 
            google_login_flow = GoogleRawLoginFlowService()
            authorization_url, state = google_login_flow.get_authorization_url()

            request.session["google_oauth2_state"] = state

            return redirect(authorization_url)

    
def google_raw_login_get_credentials() -> GoogleRawLoginCredentials:
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


class GoogleRawLoginFlowService:
    # API_URI = reverse_lazy("api:google-oauth2:login-raw:callback-raw")

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
    ]

    def __init__(self):
        self._credentials = google_raw_login_get_credentials()

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        # domain = 'settings.BASE_BACKEND_URL'
        # api_uri = self.API_URI
        # redirect_uri = f"{domain}{api_uri}"
        redirect_uri = 'http://localhost:8000/users/register_google'
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