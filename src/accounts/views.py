from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserCreateSerializer, UserLoginSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateApiView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginApiView(APIView):
    permission_classes = (AllowAny, )
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


