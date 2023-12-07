from django.urls import path
from .views import UserRegistrationAPIView, CreateAssetTransportationRequest, CreateRideTravelInfoAPIView, AssetTransportationRequestList, MatchedRidesAPIView, ApplyForRideView

urlpatterns = [
    # path('', views.index, name='index'),
    path('register-user/', UserRegistrationAPIView.as_view(), name='register_user'),
    path('create-asset-transportation-request/', CreateAssetTransportationRequest.as_view(), name='create_asset_transportation_request'),
    path('create-ride-travel-info/', CreateRideTravelInfoAPIView.as_view(), name='create_ride_travel_info'),
    path('asset-transportation-requests/', AssetTransportationRequestList.as_view(), name='asset_transportation_requests'),
    path('matched-rides/', MatchedRidesAPIView.as_view(), name='matched_rides'),
    path('apply-for-ride/<int:ride_id>/', ApplyForRideView.as_view(), name='apply_for_ride'),
]