from django.urls import path
from users.views.setter_view.setter_profile_view import SetterProfileView
from users.views.token_view.token_view import UserTokenRefreshView, UserTokenVerifyView
from users.views.user_view.user_auth_view import *
from users.views.user_view.user_crud_view import *

app_name = "users"

urlpatterns = [
    path("", UserCrudApi.as_view(), name="user_crud"),
    path("/signup", UserSignUpApi.as_view(), name="signup"),
    path("/login", UserLoginApi.as_view(), name="login"),
    path("/logout", UserLogoutApi.as_view(), name="logout"),
    path("/token/verify", UserTokenVerifyView.as_view(), name="token_verify"),
    path("/token/refresh", UserTokenRefreshView.as_view(), name="token_refresh"),
    path("/setter", SetterProfileView.as_view(), name="setter"),
    path("/profile-image", UserImageUploadView.as_view(), name="upload_profile_image"),
]
