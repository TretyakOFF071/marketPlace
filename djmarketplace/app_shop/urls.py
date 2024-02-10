from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import register_view, CustomLoginView, CustomLogoutView, MainView, UserUpdateView, balance_view, CartView, \
    pay, add_good_to_cart

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', MainView.as_view(), name='main'),
    path('profile/<int:pk>', UserUpdateView.as_view(), name='profile'),
    path('balance/', balance_view, name='balance'),
    path('add_good/<int:pk>/', add_good_to_cart, name='add_good'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/pay/<int:pk>/', pay, name='pay'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


