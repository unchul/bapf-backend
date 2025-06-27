"""
URL configuration for snack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("authentication/", include('authentication.urls')),
    path("kakao-oauth/", include('kakao_authentication.urls')),
    path("account/", include('account.urls')),
    path("account-profile/", include('account_profile.urls')),
    path("google-oauth/", include('google_authentication.urls')),
    path("naver-oauth/", include('naver_authentication.urls')),
    path("restaurant/", include('restaurants.urls')),
    path("board/", include('board.urls')),
    path("comment/", include('comment.urls')),
    path("delete-account/", include('delete_account.urls')),
    path("github-oauth/", include('github_authentication.urls')),
    path("meta-oauth/", include('meta_authentication.urls')),
    path('account-prefer/', include('account_prefer.urls')),
    path('report/', include('report.urls')),
    path('chat-history/', include('chat_history.urls')),
    path('account-scrap/', include('account_scrap.urls')),
    path('admin-user-info/', include('admin_user_info.urls')),
    path('admin-user-ban/', include('admin_user_ban.urls')),
    path('admin-user-suspend/', include('admin_user_suspend.urls')),
    path('account-alarm/', include('account_alarm.urls')),
    path('github-action-monitor/', include('github_action_monitor.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('subscribe/', include('subscribe.urls')),
]
