from rest_framework import serializers
from .models import AssetTransportationRequest, Ride, MatchedRides
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AssetTransportationRequestSerializer(serializers.ModelSerializer):
  """
  Serializer for the AssetTransportationRequest model
  """
  class Meta:
    model = AssetTransportationRequest
    fields = ['origin', 'destination', 'asset_type', 'number_of_assets', 'sensitivity', 'status', 'request_date']

class UserSerializer(serializers.ModelSerializer):
  """
  Serializer for the User model
  """
  class Meta:
    model = User
    fields = ('username', 'email', 'password', 'first_name', 'last_name')
    extra_kwargs = {
      'password': {'write_only': True}
    }

  def create(self, validated_data):
    """
    Create a new user with encrypted password and return it
    """
    user = User.objects.create_user(**validated_data)
    token, created = Token.objects.get_or_create(user=user)
    return user, token.key
  
class RideTravelInfoSerializer(serializers.ModelSerializer):
  """
   Serializer for the RideTravelInfo model
  """
  class Meta:
    model = Ride
    fields = ['origin', 'destination', 'asset_capacity', 'travel_date', 'travel_medium']

class MatchedRidesInfoSerializer(serializers.ModelSerializer):
  """
  Serializer for the MatchedRidesInfo model
  """
  username = serializers.SerializerMethodField()
  application_status = serializers.SerializerMethodField()
  class Meta:
    model = Ride
    fields = ['username', 'origin', 'destination', 'asset_capacity', 'travel_date', 'travel_medium', 'application_status']
  
  def get_username(self, obj):
    return obj.rider.username

  def get_application_status(self, obj):
    request = self.context.get("request")
    if request:
      matched_ride = MatchedRides.objects.filter(ride=obj, asset_transportation_request__requester = request.user).first()
      return matched_ride.status if matched_ride else "NOT_APPLIED"
    return "NOT_APPLIED"