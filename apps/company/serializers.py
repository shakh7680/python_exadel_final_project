from rest_framework import serializers
from apps.company.models import CompanyServiceEquipments


class CompanyServiceEquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyServiceEquipments
        exclude = ['id']