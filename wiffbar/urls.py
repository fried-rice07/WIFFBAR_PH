from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('collections/',views.collection, name="collection"),
    path('sign-up/',views.signup, name='signup'),
    path('login/',views.login, name="login"),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)