from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import AdminOnly
from .serializers import UserSerializer


@api_view(['POST'])
def registration(request):
    if not request.data.get('email'):
        return Response(
            {'message': 'Please, write your email in the request body'}
        )
    email = request.data.get('email')
    username = email.split('@')[0]
    user, created = User.objects.get_or_create(email=email, username=username)
    if not created:
        return Response({'message': 'You also registered'})

    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        'Confirmation code',
        f'This is your confirmation code: {confirmation_code}',
        settings.EMAIL_ADDRESS,
        [email],
        fail_silently=False
    )
    return Response({'message': 'Check your email for confirmation code'})


@api_view(['POST'])
def get_token(request):
    if not request.data.get('email'):
        return Response(
            {'message': 'Please, write your email in the request body'}
        )
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, email=email,
                             confirmation_code=confirmation_code)
    token = AccessToken.for_user(user=user)
    return Response({'token': str(token)})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, AdminOnly]
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
