from django.urls import path

from users.views.setter_view.setter_certification_view.setter_certification_create_list_view import (
    SetterCertificationCreateListView,
)
from users.views.setter_view.setter_certification_view.setter_certification_document_view import (
    SetterCertificationDocumentView,
)
from users.views.setter_view.setter_certification_view.setter_certificaton_view import (
    SetterCertificationView,
)
from users.views.setter_view.setter_education_view.setter_education_create_list_view import (
    SetterEducationCreateListView,
)
from users.views.setter_view.setter_education_view.setter_education_document_view import (
    SetterEducationDocumentView,
)
from users.views.setter_view.setter_education_view.setter_education_view import (
    SetterEducationView,
)
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
    path(
        "/setter/education",
        SetterEducationCreateListView.as_view(),
        name="setter_education",
    ),
    path(
        "/setter/education/<uuid:education_uuid>",
        SetterEducationView.as_view(),
        name="setter_education_detail",
    ),
    path(
        "/setter/education/<uuid:education_uuid>/document",
        SetterEducationDocumentView.as_view(),
        name="setter_education_document",
    ),
    path(
        "/setter/certification",
        setterCertificationCreateListView.as_view(),
        name="setter_certification",
    ),
    path(
        "/setter/certification/<uuid:certification_uuid>",
        SetterCertificationView.as_view(),
        name="setter_certification_detail",
    ),
    path(
        "/setter/certification/<uuid:certification_uuid>/document",
        SetterCertificationDocumentView.as_view(),
        name="setter_certification_document",
    ),
    path("/profile-image", UserImageUploadView.as_view(), name="upload_profile_image"),
]
