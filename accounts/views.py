import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_auth.registration.views import SocialLoginView


# from .models import SocialToken

def kakao_callback(request):
    app_rest_api_key = "ed28fbde773d0d8853715e943126ecc7"
    redirect_uri = "http://localhost:8100/oauth"
    user_token = request.GET.get("code")
    print(user_token)

    token_request = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
    )
    token_response_json = token_request.json()
    print(token_response_json)
    access_token = token_response_json.get("access_token")
    print(access_token)

    profile_request = requests.post(
        f"https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    print(profile_json)
    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email", None)
    profile = kakao_account.get("profile")
    nickname = profile.get("nickname")
    profile_image = profile.get("thumbnail_image_url")

    # 로직1 -> 소셜로그인에 대한 동의 및 가입이 이미 된 후에 로그인이 될 경우에는 email 체크를 해서 바로 로그인이 될 수 있도록 token 값 return
    # 로직2 -> 소셜로그인에 대한 동의 및 가입이 안된 상황에서 로그인을 할 경우 이미 예전방법으로 가입이 된 유저의 경우
    # 로직3 -> 소셜로그인에 대한 동의 및 가입이 안된 상황에서 로그인을 할 경우 가입이 된 적이 없을 경우
    user, _ = User.objects.get_or_create(username=email)
    SocialAccount.objects.get_or_create(
        user=user, provider="kakao", uid=user.id
    )
    # return JWT.generate_token(user)

    # SocialAccount.authenticate(request)
    # SocialAccount.get_provider()

    # try:
    #     # 서비스에 rest-auth 로그인
    #     data = {'code': user_token, 'access_token': access_token}
    #     accept = requests.post(
    #         f"http://127.0.0.1:8100/account/login/kakao/todjango", data=data
    #     )
    #     accept_json = accept.json()
    #     accept_jwt = accept_json.get("token")
    #
    #     # 프로필 정보 업데이트
    #     User.objects.filter(email=email).update(realname=nickname,
    #                                             email=email,
    #                                             user_type='kakao',
    #                                             profile_image=profile_image,
    #                                             is_active=True
    #                                             )
    #
    # except User.DoesNotExist:
    #     # 서비스에 rest-auth 로그인
    #     data = {'code': user_token, 'access_token': access_token}
    #     accept = requests.post(
    #         f"http://127.0.0.1:8100/account/login/kakao/todjango", data=data
    #     )
    #     accept_json = accept.json()
    #     accept_jwt = accept_json.get("token")
    #
    #     User.objects.filter(email=email).update(realname=nickname,
    #                                             email=email,
    #                                             user_type='kakao',
    #                                             profile_image=profile_image,
    #                                             is_active=True
    #                                             )

    return redirect(f'http://localhost:4200/after-login?access_token={access_token}')


class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
