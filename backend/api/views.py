from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from api.serializers import *
from .models import *
import requests, json, os
from dotenv import load_dotenv
from decimal import Decimal

#load .env file
load_dotenv()


YELP_API_KEY = os.getenv('YELP_API_KEY')
YELP_HEADERS = {'Authorization': f"Bearer {YELP_API_KEY}"}





""" api endpoints """
class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
    


class GetPlaces(APIView):
    """
    View to list all nearby places.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of nearby places.
        """

        obj = Person.objects.get(user=request.user)
        obj = obj.group if request.GET['type'] == 'group' else obj
        radius = int(obj.radius * Decimal(1609.34)) #convert radius from miles to meters

        headers = {
            'Content-Type': 'application/json',
            "X-Goog-Api-Key": os.getenv('GOOGLE_API_KEY'),
            "X-Goog-FieldMask": "places.id,places.displayName,places.location,places.googleMapsUri,places.rating,places.userRatingCount," \
            "places.internationalPhoneNumber,places.priceLevel,places.regularOpeningHours,places.currentOpeningHours,places.reviews,places.photos,places.editorialSummary"
        }

        data = json.dumps({
            "includedTypes": ["restaurant"],
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                "center": {
                    "latitude": obj.latitude,
                    "longitude": obj.longitude},
                "radius": radius
                }
            }
        })

        r = requests.post('https://places.googleapis.com/v1/places:searchNearby', data=data, headers=headers)
        data = json.loads(r.content)['places']


        obj.places = json.dumps(data)
        obj.save()

        return Response(data)
    



""" group endpoints """
class UpdateAddressView(UpdateAPIView):
        """
        An endpoint for changing address.
        """
        serializer_class = UpdateAddressSerializer
        model = Group
        permission_classes = [permissions.IsAuthenticated]

        def get_object(self, queryset=None):
            obj = Person.objects.get(user=self.request.user).group
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # set_password also hashes the password that the user will get
                self.object.address = serializer.data.get("address")
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'address updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GetGroupPlaces(APIView):
    """
    View to list all nearby places.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of nearby places.
        """

        obj = Person.objects.get(user=request.user)
        obj = obj.group if request.GET['type'] == 'group' else obj

        return Response(obj.places)




""" auth endpoints """
class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)