from rest_framework import viewsets, status
from apps.company.models import CompanyServiceEquipments
from apps.company import permissions
from apps.company import serializers


class CompanyServiceEquipmentsViewSet(viewsets.ModelViewSet):
    queryset = CompanyServiceEquipments.objects.all()
    serializer_class = serializers.CompanyServiceEquipmentsSerializer
    permission_classes = [permissions.CompanyPermission]


