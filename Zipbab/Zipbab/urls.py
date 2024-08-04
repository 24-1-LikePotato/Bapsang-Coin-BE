from django.contrib import admin
from django.urls import path,include, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="멋쟁이 감자처럼",
        default_version='v.24-07-31',
        description="멋쟁이 감자처럼 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="likelion@inha.edu"), # 부가정보
        license=openapi.License(name="backend"),     # 부가정보
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('account/', include('account.urls')),
    path('price/' ,include('price.urls')),
    path('util/',include('util.urls')),
    # Swagger url
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)