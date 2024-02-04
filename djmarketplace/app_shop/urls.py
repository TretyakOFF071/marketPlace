from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import register_view, CustomLoginView, CustomLogoutView, MainView, UserUpdateView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', MainView.as_view(), name='main'),
    path('profile/<int:pk>', UserUpdateView.as_view(), name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


