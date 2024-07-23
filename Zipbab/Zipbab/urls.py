from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('account/', include('account.urls')),
    path('price/' ,include('price.urls')),
    path('util/',include('util.urls')),
]
 