from django.urls import path
from . import views

urlpatterns = {
    path('from-camera/', views.receive_frames),
}
