from django.contrib import admin
from django.urls import path, include
from accounts.views import kakao_callback, KakaoToDjangoLogin

urlpatterns = [
    # 어드민 페이지
    path('admin/', admin.site.urls),

    # 로그인
    path('account/', include('rest_auth.urls')),
    path('account/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('', include('django.contrib.auth.urls')),

    # path('account/login/kakao/', kakao_login, name='kakao_login'),
    path('oauth', kakao_callback, name='kakao_callback'),
    path('account/login/kakao/todjango', KakaoToDjangoLogin.as_view(), name='kakao_todjango_login'),
]
