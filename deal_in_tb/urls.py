from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [


    # Store Service
    path('api/', include('store_service.urls')),
    path('api/', include('auth_service.urls')),


    #Payment Gateway
    # path('trans_token/', views.TransactionToken, name='trans_token'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)