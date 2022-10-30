from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #base
    path('base/',views.base, name="base"),

    path('', views.home, name='home'),
    path('collections/',views.collection, name="collection"),
    path('sign-up/',views.signup, name='signup'),
    path('login/',views.login_user, name="login"),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name="add-to-cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('logout/', views.log_out, name="logout"),
    path('password_change', views.password_change, name="password_change"),
    path('profile/', views.profile, name="profile"),
    path('edit-profile/<int:pk>/', views.edit_profile, name="edit-profile"),

    path('delete-product<int:pk>/',views.delete_product, name="delete-product"),

    #add to cart 
    path('update-item/',views.updateItem, name="update-item"),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)