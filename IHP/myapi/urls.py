# myapi/urls.py
from django.urls import path
from .views import register_user,CustomTokenObtainPairView,mark_as_spam,search_phone_number,create_phone_number,search_by_name
from django.urls import path


urlpatterns = [
    path('register/', register_user, name='register'),
     path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('mark_as_spam/', mark_as_spam, name='mark_as_spam'),
     path('search_phone_number/', search_phone_number, name='search_phone_number'),
     path('add_to_global_dataset/', create_phone_number, name='add_to_global_dataset'),
     path('search_by_name/',search_by_name, name='search_by_name'),
    
]

