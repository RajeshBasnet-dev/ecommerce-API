from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import GlobalSearchView
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # Map root URL to IndexView
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/<int:id>/', views.product_detail_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('orders/', views.orders_view, name='orders'),
    path('profile/', views.profile_view, name='profile'),
    path('api/auth/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/messages/', include('apps.messaging.urls')),
    path('api/search/', GlobalSearchView.as_view(), name='global-search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)