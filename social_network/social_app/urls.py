from django.urls import path
from .views import SignupView, LoginView, UserSearchViewSet, FriendRequestAPIView

urlpatterns = [
    path("user-search/", UserSearchViewSet.as_view(), name="user_search"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("friend-requests/", FriendRequestAPIView.as_view(), name="friend-request-api"),
]
