from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserListView, UserDetailView, LogoutView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
]