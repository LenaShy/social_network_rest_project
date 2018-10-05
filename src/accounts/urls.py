from django.urls import path, include

from .views import UserCreateApiView, UserLoginApiView

urlpatterns = [
    path('register/', UserCreateApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
]
