from .views import register_user,user_details,referrals,UserDetailsAPIView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .swagger import schema_view


urlpatterns = [
    # This line of code is defining a URL pattern using Django's `path` function. It maps the URL path
    # 'register/' to the `register_user` view function. So, when a user navigates to the 'register/'
    # endpoint in the application, the `register_user` function will be called to handle the request.
    path('register/', register_user),
    path('user_details/', user_details),
    path('referrals/', referrals),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('user_details/<int:id>/', UserDetailsAPIView.as_view(), name='user-details'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
