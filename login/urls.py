# loginApp/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import api_root,  RegisterView, LoginView, LogoutView, UserProfileView, UserListView, PasswordResetVIEW



urlpatterns = [
    path('', api_root),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("reset-passsword/", PasswordResetVIEW.as_view(), name="password-reset"),
    path("user-list/", UserListView.as_view(), name="user-list"),
    path("profile/", UserProfileView.as_view(), name="profile")
]
    

urlpatterns = format_suffix_patterns(urlpatterns)