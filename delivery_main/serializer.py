from django.db.models.base import Model
from rest_framework import serializers
from .models import App

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['name', '__all__']