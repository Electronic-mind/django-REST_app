from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import authenticate, get_user_model, login
import jwt

from .utils import generate_access_token
from user_management.serializers import UserLoginSerializer, UserRegistrationSerializer
from restaurant_site import settings



# The view for registering new users
class UserRegistrationAPIView(APIView):
    '''Sign up as a new user'''
    # set the serializer, authentication, and permission classes for this API
    serializer_class = UserRegistrationSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)


    def get(self, request):
        # Handle GET request
        return Response('Please enter your id, name and password.')
    
    def post(self, request):
        # Handle POST requests
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # save the informations in the serializer to register a new user
            new_user = serializer.save()
            if new_user:
                # Generate access token with the employee id in the payload
                access_token = generate_access_token(new_user) 

                # Generate cookie with the new token as the value
                data = { 'access_token': access_token }
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)

                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        # Handle GET requests
        content = {"message": "Please enter your credentials"}
        return Response(content)
    

    def post(self, request):
        # Handle POST requests
        emp_id = request.data.get('employee_id', None)
        user_password = request.data.get('password', None)

        # Check if the id and password are provided
        if not emp_id:
            raise AuthenticationFailed('An employee number is needed.')
        if not user_password:
            raise AuthenticationFailed("A user password is needed.")
        
        # Authenticate the user with the given credentials
        user_instance = authenticate(username=emp_id, password=user_password)

        if not user_instance:
            raise AuthenticationFailed("User not found.")
        

        if user_instance.is_active:
            # Generate an access token for the user 
            user_access_token = generate_access_token(user_instance)
            response = Response()
            response.set_cookie(key='access_token', value=user_access_token, httponly=True)
            login(request, user_instance)
            response.data = {
                'access_token': user_access_token
            }
            return response

        return Response({
            'message': 'Something went wrong.'
        })
    

class UserViewAPI(APIView):
    '''Here are the user details'''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        # Check the user access token
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        # get the user Id from the token and query the user information
        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()
        user_serializer = UserRegistrationSerializer(user)
        return Response({ 'emp_id':user_serializer.data['emp_id'] , 'name': user_serializer.data['name']})


class UserLogoutViewAPI(APIView):
	authentication_classes = (JWTAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
          # get the user token from the cookies
		user_token = request.COOKIES.get('access_token', None)
		if user_token:
			response = Response()
			response.delete_cookie('access_token')
			response.data = {
				'message': 'Logged out successfully.'
			}
			return response
		response = Response()
          
        # if the cookies don't exist
		response.data = {
			'message': 'User is already logged out.'
		}
		return response
