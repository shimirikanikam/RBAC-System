from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import userLogin

urlpatterns = [ 
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.userLogin, name="user_token"),
    path('add_user/', views.add_user,name="add_user"),
    path('remove_user/', views.remove_user,name="remove_user"),
    path('update_user/',views.update_user,name= "update_user"),
    path('add_api/',views.add_api,name= "add_api"),
    path('remove_api/', views.remove_api,name= "remove_api"),
    path('update_api/', views.update_api,name= "update_api"),
    path('view_api/', views.view_api,name= "view_api"),
    path('admin/', views.add_user, name = "admin"),
    


    
]