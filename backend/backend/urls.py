from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from points.web_views import home_view, points_list_view, messages_list_view
from backend.health import health_check

urlpatterns = [
    path("", home_view, name="home"),
    path("points/", points_list_view, name="points-list"),
    path("messages/", messages_list_view, name="messages-list"),
    path("health/", health_check, name="health-check"),
    
    path("admin/", admin.site.urls),

    # Документация
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # авторизация
    path("api/auth/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),

    # Приложения
    path("api/users/", include("users.urls")),
    path("api/", include("points.urls")),
]

if settings.DEBUG:
    import silk  # noqa: F401
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)