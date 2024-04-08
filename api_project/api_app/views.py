from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer,ReferralSerializer,UserRegistrationSerializer
from .models import User
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from rest_framework.generics import RetrieveAPIView
from . models import Referral
from .utils import generate_referral_code
from rest_framework.pagination import PageNumberPagination

import random
# The `register_user` function is a view in a Django REST framework API that handles the registration
# of a new user. Here's a breakdown of what it does:

@api_view(['POST'])
def register_user(request):
  try:
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        referral_code = request.data.get('referral_code')

        # Check if required fields are provided
        if not (name and email and password):
            return Response({'error': 'Name, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email address is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate referral code for the new user
        referral_code = generate_referral_code()

        # Hash the password
        hashed_password = make_password(password)

        # Create the user
        user = User.objects.create(name=name, email=email, password=hashed_password, referral_code=referral_code)

        # If referral code is provided, create a Referral instance and increment referring user's points
       # This block of code is handling the referral system logic when a new user is registered with a
       # referral code. Here's a breakdown of what it does:
        if referral_code:
            referring_user = User.objects.filter(referral_code=request.data.get('referral_code')).first()
           # This block of code is handling the referral system logic when a new user is registered
           # with a referral code. Here's a breakdown of what it does:
            if referring_user:
                Referral.objects.create(referrer=referring_user, referee=user)
                referring_user.points += 100  # Increment referring user's points
                referring_user.save()

        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    serializer = UserDetailsSerializer(request.user)
    return Response(serializer.data)



class ReferralPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def referrals(request):
    user = request.user

    # Retrieve referrals associated with the authenticated user
    referrals = Referral.objects.filter(referrer=user)

    # Pagination
    paginator = PageNumberPagination()
    paginated_referrals = paginator.paginate_queryset(referrals, request)

    # Serialize the paginated referrals
    serializer = ReferralSerializer(paginated_referrals, many=True)

    return paginator.get_paginated_response(serializer.data)

# The `UserDetailsAPIView` class retrieves details of a user with authentication required.

class UserDetailsAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' 