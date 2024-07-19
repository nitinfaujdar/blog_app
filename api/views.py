from rest_framework.generics import GenericAPIView, ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *

UserModel = get_user_model()

def get_new_temp_username(name):
    return f"{name}{(str(uuid.uuid4().hex))[:6]}"

# Registration API for new users

class RegisterView(CreateAPIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        if not email or not password or not name:
            return Response({"Error": "Email, Password and Name are required."}, status=status.HTTP_400_BAD_REQUEST)
        if not UserModel.objects.filter(email=email).exists():
            user_model = UserModel.objects.create(
                username=get_new_temp_username(name), email=email, password=password, 
                first_name=name
            )
            return Response({"message": "Registration successfull"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": "User with this email already exist"}, status=status.HTTP_400_BAD_REQUEST)

# Login API for existing users

class LoginView(CreateAPIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"Error": "Email and Password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.get(email=email)
        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successfull", "token": token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": "User with this email already exist"}, status=status.HTTP_400_BAD_REQUEST)

class BlogsView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Blog posted successfully", "data": serializer.data}, 
                        status=status.HTTP_201_CREATED)
    
    def get(self, request):
        obj = Post.objects.all().order_by('-published_date')
        page = self.paginate_queryset(obj)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return Response({"message": "Blogs retrieved successfully", "data": response.data},
                        status=status.HTTP_200_OK)
    
    def patch(self, request):
        try:
            post = Post.objects.get(id=request.data.get('blog'))
        except Post.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid Blog ID supplied!"})
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Blog updated successfully", "data": serializer.data}, 
                        status=status.HTTP_200_OK)
    
    def delete(self, request):
        try:
            post = Post.objects.get(id=request.data.get('blog'))
        except Post.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid Blog ID supplied!"})
        post.delete()
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_200_OK)

class LikeBlogsView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            post = Post.objects.get(id=request.data.get('blog'))
        except Post.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid Blog ID supplied!"})
        obj, _ = Like.objects.get_or_create(author=request.user, post=post)
        return Response({"message": "Blog liked successfully"}, status=status.HTTP_200_OK)

class CommentView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Comment posted successfully", "data": serializer.data}, 
                        status=status.HTTP_201_CREATED)