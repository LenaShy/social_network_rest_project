from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        SerializerMethodField,
                                        )

from .models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    image = HyperlinkedIdentityField

    class Meta:
        model = Post
        fields = ('title',
                  'content',
                  'publish',
                  'image'
                  )


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug'
    )
    user = SerializerMethodField()
    likes = SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('url',
                  'id',
                  'user',
                  'title',
                  'slug',
                  'publish',
                  'likes',
                  'image',
                  )

    def get_user(self, obj):
        return str(obj.user.username)

    def get_likes(self, obj):
        return obj.likes.count()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image


class PostDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    html = SerializerMethodField()
    image = SerializerMethodField()
    likes = SerializerMethodField()
    like_url = HyperlinkedIdentityField(
        view_name='posts-api:like',
        lookup_field='slug'
    )

    class Meta:
        model = Post
        fields = ('id',
                  'user',
                  'title',
                  'slug',
                  'html',
                  'content',
                  'publish',
                  'image',
                  'like_url',
                  'likes',
                  )

    def get_user(self, obj):
        return str(obj.user.username)

    def get_html(self, obj):
        return obj.get_markdown()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_likes(self, obj):
        return obj.likes.count()