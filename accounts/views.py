import json

from django.shortcuts import redirect, HttpResponse
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialToken, SocialApp
import requests


# from .models import SocialToken

#
# def kakao_login(request):
#     app_rest_api_key = ""
#     redirect_uri = "http://127.0.0.1:8000/account/login/kakao/callback"
#
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
#     )


def kakao_callback(request):
    user = request.user
    app_rest_api_key = ""
    redirect_uri = "http://localhost:8100/oauth"
    user_token = request.GET.get("code")

    token_request = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
    )
    token_response_json = token_request.json()
    print(token_response_json)
    access_token = token_response_json.get("access_token")
    print(access_token)

    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email", None)
    profile = kakao_account.get("profile")
    nickname = profile.get("nickname")
    profile_image = profile.get("thumbnail_image_url")  # 사이즈 'thumbnail_image_url' < 'profile_image_url'
    # print('image', profile_image)

    # social_token = SocialToken(account_id=user.id, app_id=SocialApp.id)
    # social_token.save()

    return HttpResponse(json.dumps(
        {
            'access_token': access_token,
            'email': email,
            'nickname': nickname,
            'profile': profile,
            'kakao_account': kakao_account,
            'profile_image': profile_image,
        }
    ))


class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
