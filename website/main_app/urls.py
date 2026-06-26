
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "main_app"

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_request, name="logout"),
    path('login/', views.login_request, name="login"),

    path('emergency_contact/', views.emergency_contact, name="emergency_contact"),
    path("create_contact/", views.create_contact , name="create_contact"),
    path("update_contact/<str:pk>/", views.update_contact, name="update_contact"),
    path("delete_contact/<str:pk>/", views.delete_contact, name="delete_contact"),
    path("emergency/", views.emergency, name="emergency"),


    path("city_map/", views.city_map, name="city_map"),
    path("find_me/", views.find_me, name="find_me"),


    path("helpline_numbers/", views.helpline_numbers, name="helpline_numbers"),
    path('violent/', views.violent, name='violent'),
    path('send-location/', views.send_location, name='send_location'),
    path('live-camera/', views.live_camera, name='live_camera'),
    path('live-detect/', views.live_detect, name='live_detect'),
    path("index/", views.index, name="index"),
    path("translate/", views.translate, name="translate"),
    path("test-email/", views.test_email, name="test_email"),

] 


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)