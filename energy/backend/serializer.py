from rest_framework import serializers

from backend.models import NemData


class NemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NemData
        fields = '__all__'
