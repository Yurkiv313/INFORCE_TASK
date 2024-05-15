from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RestaurantViewSet, MenuViewSet, MenuViews, EmployeeCreateAPIView, VoteUpsertAPIView, \
    MostVotedRestaurantMenuAPIView

get_restaurant = RestaurantViewSet.as_view(
    {
        "get": "get_restaurant"
    }
)

create_restaurant = RestaurantViewSet.as_view(
    {
        "post": "create_restaurant"
    }
)

get_menu = MenuViewSet.as_view(
    {
        "get": "get_menus"
    }
)

create_menu = MenuViewSet.as_view(
    {
        "post": "create_menu"
    }
)

todays_menu = MenuViewSet.as_view(
    {
        "get": "todays_menu"
    }
)

get_menu_by_day_of_week = MenuViews.as_view(
    {
        "get": "get_menu_by_day_of_week",
    }
)


SPECTACULAR_SETTINGS = {
    'TITLE': 'LUNCH API',
    'DESCRIPTION': 'LUNCH API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/restaurants/", get_restaurant, name="get_restaurant"),
    path("api/restaurants/", create_restaurant, name="create_restaurant"),
    path("api/menu/", get_menu, name="get_menu"),
    path("api/menu/", create_menu, name="create_menu"),
    path("api/menu/current", todays_menu, name="todays_menu"),
    path("api/menu/day/<int:pk>", get_menu_by_day_of_week, name="get_menu_by_day_of_week"),
    path('employees/', EmployeeCreateAPIView.as_view(), name='employee-create'),
    path('votes/', VoteUpsertAPIView.as_view({'get': 'get_object', 'put': 'put'}), name='votes'),
    path('votes/top/', MostVotedRestaurantMenuAPIView.as_view({'get': 'get'}), name='most-voted-restaurant-menu'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
