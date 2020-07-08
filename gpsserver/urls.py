
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
#- from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from .views import schema_view as schema_view_old
from .views import TransportView, TransportDataCurrentPosView, TrackDataView

schema_view = get_schema_view(
   openapi.Info(
      title="GPS-GSM Server API",
      default_version='v1.0',
      description="GPS-GSM Server API",
      # terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # url(r'^docs/$', schema_view, name='schema_view_old'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #- path('hello/', HelloView.as_view(), name='hello'),
    path('api/trackers/', TransportView.as_view()),
    path('api/track_data/<int:id>', TrackDataView.as_view()),
    path('api/tracker_current_position/<int:id>', TransportDataCurrentPosView.as_view()),
]

#- urlpatterns += staticfiles_urlpatterns()
