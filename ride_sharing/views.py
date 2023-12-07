from django.shortcuts import render
from datetime import date
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import AssetTransportationRequest, Ride, MatchedRides
from .serializers import AssetTransportationRequestSerializer, UserSerializer, RideTravelInfoSerializer, MatchedRidesInfoSerializer
from .pagination import PaginationClass
# Create your views here.

class UserRegistrationAPIView(APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user, token = serializer.save()
      return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAssetTransportationRequest(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    serializer = AssetTransportationRequestSerializer(data=request.data)
    if serializer.is_valid():
      asset_transportation_request = serializer.save(requester = request.user)
      matched_rides = Ride.objects.filter(
        origin = asset_transportation_request.origin,
        destination = asset_transportation_request.destination,
        travel_date = asset_transportation_request.request_date,
      )
      for ride in matched_rides:
        MatchedRides.objects.create(ride = ride, asset_transportation_request = asset_transportation_request)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class CreateRideTravelInfoAPIView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, *args, **kwargs):
    serializer = RideTravelInfoSerializer(data=request.data)
    if serializer.is_valid():
      ride = serializer.save(rider = request.user)
      matching_requests = AssetTransportationRequest.objects.filter(
        origin = ride.origin,
        destination = ride.destination,
        request_date = ride.travel_date
      )
      for request in matching_requests:
        MatchedRides.objects.create(ride = ride, asset_transportation_request = request)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssestTransportationRequestFilter(filters.FilterSet):
  class Meta:
    model = AssetTransportationRequest
    fields = {
      'status': ['exact'],
      'asset_type': ['exact'],
      'request_date': ['lte', 'gte']
    }

class AssetTransportationRequestList(generics.ListAPIView):
  serializer_class = AssetTransportationRequestSerializer
  permission_classes = [IsAuthenticated]
  filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
  filterset_class = AssestTransportationRequestFilter
  ordering_fields = ['request_date']
  ordering = ['-request_date']
  pagination_class = PaginationClass

  def get_queryset(self):
    today = date.today()
    query_set = AssetTransportationRequest.objects.filter(requester = self.request.user)
    for request in query_set:
      if request.request_date < today and request.status != 'EXPIRED':
        request.status = 'EXPIRED'
        request.save()
    return query_set


class MatchedRidesAPIView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]
  pagination_class = PaginationClass
  serializer_class = MatchedRidesInfoSerializer

  def get_queryset(self):
    matched_rides = MatchedRides.objects.filter(asset_transportation_request__requester = self.request.user)

    ride_ids = matched_rides.values_list('ride__id', flat=True).distinct()

    return Ride.objects.filter(id__in = ride_ids)

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context.update({'request': self.request})
    return context

class ApplyForRideView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, ride_id):
    try:
      print(request.user, ride_id)
      matched_ride = MatchedRides.objects.get(ride_id = ride_id, asset_transportation_request__requester = request.user)
      matched_ride.status = 'APPLIED'
      matched_ride.save()
      return Response({'message': 'Applied for ride successfully'}, status=status.HTTP_200_OK)
    except MatchedRides.DoesNotExist:
      return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)