from rest_framework import serializers

from backend.models import NemData


class NemSerializer(serializers.ModelSerializer):
    """
    Serializer for NewData model. It helps in serialization and deserialization.
    """
    class Meta:
        model = NemData
        fields = '__all__'
