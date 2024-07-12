# Import necessary modules and classes
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser, SpamNumber, PhoneNumber, Name
from .serializers import UserSerializer, CustomUserSerializer, SpamNumberSerializer, PhoneNumberSerializer

import re  # Import regular expression module for phone number validation

# API endpoint to mark a phone number as spam
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access this endpoint
def mark_as_spam(request):
    """
    API endpoint to mark a phone number as spam.

    Parameters:
    - request: HTTP request object containing the phone_number in the request data.

    Returns:
    - Response: JSON response indicating success or failure.
    """
    phone_number = request.data.get('phone_number')
    if phone_number:
        # Increment spam count for unregistered number
        spam_number, created = SpamNumber.objects.get_or_create(phone_number=phone_number)
        spam_number.spam_count += 1
        spam_number.save()
        return Response({'message': f'Number {phone_number} marked as spam.'})
    else:
        return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint to register a new user
@api_view(['POST'])
@permission_classes([AllowAny])  # Any user can access this endpoint
def register_user(request):
    """
    API endpoint to register a new user.

    Parameters:
    - request: HTTP request object containing user data including phone_number.

    Returns:
    - Response: JSON response indicating success or failure.
    """
    phone_number = request.data.get('phone_number')
    if phone_number:
        # Create user with data from the request
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            
            # Check if any spam numbers match the newly registered user's phone number
            spam_numbers = SpamNumber.objects.filter(phone_number=phone_number)
            if spam_numbers.exists():
                # Sync spam count from SpamNumber model to user profile
                user.spam = sum(spam_number.spam_count for spam_number in spam_numbers)
                user.save()
                # Clear spam count from SpamNumber model
                spam_numbers.delete()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint to search users by name
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access this endpoint
def search_by_name(request):
    """
    API endpoint to search users by name.

    Parameters:
    - request: HTTP request object containing the 'name' query parameter.

    Returns:
    - Response: JSON response containing user details with spam count.
    """
    name = request.query_params.get('name', None)
    if name:
        # Retrieve the user by name
        users = CustomUser.objects.filter(username__icontains=name)
        serializer = CustomUserSerializer(users, many=True)
        
        # Create a list to store user details with spam count
        users_with_spam = []
        for user in serializer.data:
            phone_number = user['phone_number']
            
            # Retrieve the spam count from SpamNumber model
            try:
              spam_number = SpamNumber.objects.get(phone_number=phone_number)
              spam_count = spam_number.spam_count
            except SpamNumber.DoesNotExist:
              spam_count = 0
            
            # Append user details along with spam count to the list
            user['spam'] = spam_count
            users_with_spam.append(user)
        
        return Response(users_with_spam)
    else:
        return Response({'error': 'Name parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint to search for a phone number
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access this endpoint
def search_phone_number(request):
    """
    API endpoint to search for a phone number.

    Parameters:
    - request: HTTP request object containing the 'phone_number' query parameter.

    Returns:
    - Response: JSON response containing the phone number status and spam count.
    """
    phone_number = request.query_params.get('phone_number')
    
    # Validate phone number
    if not phone_number:
        return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the phone number is a 10-digit positive integer
    if not re.fullmatch(r'\d{10}', phone_number):
        return Response({'error': 'Phone number must be a 10-digit positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(phone_number=phone_number)
        user_serializer = CustomUserSerializer(user)
        try:
            spam_number = SpamNumber.objects.get(phone_number=phone_number)
            spam_count = spam_number.spam_count
        except SpamNumber.DoesNotExist:
            spam_count = 0

        return Response({
            'status': 'registered',
            'user': user_serializer.data,
            'spam_count': spam_count
        }, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        try:
            spam_number = SpamNumber.objects.get(phone_number=phone_number)
            return Response({
                'status': 'not registered',
                'spam_count': spam_number.spam_count
            }, status=status.HTTP_200_OK)
        except SpamNumber.DoesNotExist:
            return Response({
                'status': 'not registered',
                'spam_count': 0
            }, status=status.HTTP_200_OK)

# API endpoint to create a phone number
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access this endpoint
def create_phone_number(request):
    """
    API endpoint to create a phone number.

    Parameters:
    - request: HTTP request object containing the phone number data.

    Returns:
    - Response: JSON response indicating success or failure.
    """
    if request.method == 'POST':
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Token obtain endpoint for authentication
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
