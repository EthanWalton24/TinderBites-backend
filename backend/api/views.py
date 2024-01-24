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
        #get person/group calling api
        obj = Person.objects.get(user=request.user)
        # obj = obj.group if request.GET['type'] == 'group' else obj

        if obj.use_address:
            latitude = obj.latitude
            longitude = obj.longitude
        else:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']

        #api parameters
        radius = int(obj.radius * Decimal(1609.34)) #convert radius from miles to meters
        category = 13065 #restaurants
        limit = 50
        fields = [
            'fsq_id',
            'name',
            'location',
            'geocodes',
            'distance',
            'description',
            'tel',
            'hours',
            'rating',
            'price',
            'menu',
            'tips',
            'photos'
        ]

        #create and send api request
        url = f"https://api.foursquare.com/v3/places/search?ll={latitude}%2C{longitude}&radius={radius}&categories={category}&limit={limit}&fields={','.join(fields)}&sort=DISTANCE"
        headers = {
            "accept": "application/json", 
            "Authorization": os.getenv('FOURSQUARE_API_KEY')
        }
        req = requests.get(url, headers=headers)
        res = json.loads(req.content)['results']

        #remove duplicate restaurants (multiple McDonald's etc.) and remove places without photos or ratings
        data = []
        for place in res:
            if not any([place['name'] == d['name'] for d in data]):
                if len(place['photos']) > 0 and 'rating' in place:
                    data.append(place)
        
        #save the places data in group if called by a group
        if request.GET['type'] == 'group':
            obj.places = json.dumps(data)
            obj.save()

        return Response(data)
    

class Settings(APIView):
    """
    View to get all users settings.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return users settings.
        """
        #get person/group calling api
        obj = Person.objects.get(user=request.user)
        # obj = obj.group if request.GET['type'] == 'group' else obj

        data = {
            'longitude': obj.longitude,
            'latitude': obj.latitude,
            'address': obj.address,
            'radius': obj.radius,
            'use_address': obj.use_address
        }

        return Response(data)
    

    def post(self, request, format=None):
        """
        Set users settings
        """
        obj = Person.objects.get(user=request.user)
        # obj = obj.group if request.GET['type'] == 'group' else obj

        try:
            d = json.loads(request.body)

            obj.address = d['address']
            obj.latitude = d['latitude']
            obj.longitude = d['longitude']
            obj.radius = d['radius']
            obj.use_address = d['use_address']
            obj.save()

            return Response({'status': 'ok'})

        except:
            return Response({'status': 'error'})
        


class Profile(APIView):
    """
    View to get users profile.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return users settings.
        """
        #get person/group calling api
        obj = Person.objects.get(user=request.user)
        # obj = obj.group if request.GET['type'] == 'group' else obj

        data = {
            'username': obj.user.username,
            'name': obj.user.first_name,
            'email': obj.user.email,
        }

        return Response(data)
    

    def post(self, request, format=None):
        """
        Set users settings
        """
        obj = Person.objects.get(user=request.user)
        # obj = obj.group if request.GET['type'] == 'group' else obj

        try:
            d = json.loads(request.body)

            obj.user.username = d['username']
            obj.user.first_name = d['name']
            obj.user.email = d['email']
            obj.user.save()

            return Response({'status': 'ok'})

        except:
            return Response({'status': 'error'})




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