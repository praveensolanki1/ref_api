from rest_framework import serializers
from .models import User,Referral
from django.core.validators import validate_email

# The `UserRegistrationSerializer` class defines a serializer for user registration with fields for
# name, email, password, and referral code.
class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    class Meta:
        model = User
        fields = ['name', 'email', 'password','referral_code']
        


# The `UserDetailsSerializer` class is a Django REST framework serializer for the User model with
# fields for name, email, referral code, registration timestamp, and points.
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'referral_code', 'timestamp_of_registration','points']        


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referee', 'timestamp']      



            