from django.contrib.auth import authenticate

from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from .serializers import *
from firebase_admin import auth, db
import firebase_admin
from events.models import Category
from events.serializers import CategorySerializer


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():

            firebase_user = auth.create_user(
                email=request.data.get('email'),
                password=request.data.get('password')
            )

            serializer.save(firebase_uid=firebase_user.uid)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            raise Http404

        user = authenticate(email=email, password=password)
        if not user:
            raise Http404
        token,_ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class UploadPhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, pk):
        serializer = ProfilePhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save()

            profile = UserProfile.objects.get(pk=pk)
            profile.photo = photo
            profile.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user = request.user
        try:
            current_password = request.data['current_password']
            new_password = request.data['new_password']
        except KeyError:
            raise Http404

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
        else:
            raise Http404

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})

    @staticmethod
    def get(request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FirebaseTokenView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put(self, request):
        key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        Token.objects.filter(key=key).update(key=request.data["key"])
        try:
            token = Token.objects.get(key=request.data["key"])
        except Token.DoesNotExist:
            raise Http404

        return Response({"key": token.key}, status=status.HTTP_200_OK)
