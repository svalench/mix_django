from django.urls import path

from user.views import get_user_country, CustomAuthToken, Logout, create_auth, activation_accaunt
from user.viewset import DataUserViewSet, ChangePasswordView, UserAuthTokenUpdate

urlpatterns = [
        path('country', get_user_country, name='get_user_country'),
        # auth
        path('sign_in/', CustomAuthToken.as_view()),
        path('sign_out/', Logout.as_view()),
        path('sign_up/', create_auth),
        path('cabinet/mydata/', DataUserViewSet.as_view(), name='get_data_user'),
        path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
        path(r'activate/<slug:uidb64>/<slug:token>/', activation_accaunt, name='activate'),
        path('update/token/', UserAuthTokenUpdate.as_view(), name='update_token'),
]