from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('delivery_main', views.AppViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('recommand/', views.recommand, name='recommand'),
    path('recommand/good', views.good, name='good'),
    path('recommand/bad', views.bad, name='bad'),
    path('', include(router.urls))
]