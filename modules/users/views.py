"""
Views for the Users module.
"""

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import User, UserProfile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer,
)
from shared.utils import format_response


@extend_schema(
    tags=['Authentication'],
    request=UserRegistrationSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description='Bad request'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user account.

    Creates a new user with the provided credentials and
    returns the user data along with JWT tokens.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            format_response(
                {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                },
                message="User registered successfully"
            ),
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema(
    tags=['Authentication'],
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(description='Login successful'),
        401: OpenApiResponse(description='Invalid credentials'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate a user and return JWT tokens.
    """
    serializer = UserLoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response(
            format_response(
                {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                },
                message="Login successful"
            ),
            status=status.HTTP_200_OK
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_401_UNAUTHORIZED
    )


@extend_schema(
    tags=['User Profile'],
    responses={200: UserSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get the current authenticated user's profile.
    """
    serializer = UserSerializer(request.user)
    return Response(format_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    tags=['User Profile'],
    request=UserSerializer,
    responses={200: UserSerializer}
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    Update the current user's profile information.
    """
    partial = request.method == 'PATCH'
    serializer = UserSerializer(request.user, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(
            format_response(serializer.data, message="Profile updated successfully"),
            status=status.HTTP_200_OK
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema(
    tags=['User Profile'],
    request=UserProfileSerializer,
    responses={200: UserProfileSerializer}
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_preferences(request):
    """
    Update the current user's cycle preferences and settings.
    """
    profile = request.user.profile
    partial = request.method == 'PATCH'
    serializer = UserProfileSerializer(profile, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(
            format_response(serializer.data, message="Preferences updated successfully"),
            status=status.HTTP_200_OK
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema(
    tags=['User Profile'],
    request=PasswordChangeSerializer,
    responses={200: OpenApiResponse(description='Password changed successfully')}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change the current user's password.
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(
            format_response(None, message="Password changed successfully"),
            status=status.HTTP_200_OK
        )
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )
