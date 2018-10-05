from django.db.models import Q

from rest_framework.generics import (CreateAPIView,
                                     DestroyAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView
                                     )
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response


from .serializers import (PostDetailSerializer,
                          PostListSerializer,
                          PostCreateUpdateSerializer
                          )

from .models import Post
from .permissions import IsOwnerOrReadOnly


class PostCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = (AllowAny,)


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly, )

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly, )


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'content', 'user__first_name', 'user__last_name')

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list


class PostLikeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        obj = Post.objects.get(slug=slug)
        user = request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
                liked = True
            updated = True
        data = {
            'updated': updated,
            'liked': liked
        }
        return Response(data)


