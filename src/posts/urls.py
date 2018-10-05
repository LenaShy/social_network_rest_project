from django.urls import path

from .views import (
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostLikeApiView
)

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/edit/', PostUpdateAPIView.as_view(), name='update'),
    path('<slug:slug>/delete/', PostDeleteAPIView.as_view(), name='delete'),
    path('<slug:slug>/like/', PostLikeApiView.as_view(), name='like'),
]
