from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.account import models as account_model
from apps.company import models
from apps.company import permissions
from apps.company import serializers


class CompanyLocationViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = account_model.Location.objects.all()
    serializer_class = serializers.CompanyLocationSerializer
    permission_classes = [permissions.CompanyPermission]

    def get_serializer_context(self):
        return {"request": self.request}


class CompanyServiceEquipmentsViewSet(viewsets.ModelViewSet):
    queryset = models.CompanyServiceEquipments.objects.all()
    serializer_class = serializers.CompanyServiceEquipmentsSerializer
    permission_classes = [permissions.CompanyPermission]

    def create(self, request, *args, **kwargs):
        company = self.request.user
        images = dict(self.request.data).get("images")
        print(images)
        equipment_model = self.request.data.get("equipment_model")
        additional_info = self.request.data.get("additional_info")
        equipment = self.queryset.create(company=company, equipment_model=equipment_model,
                                         additional_info=additional_info)
        data = serializers.CompanyServiceEquipmentsSerializer(instance=equipment,
                                                              context={"request": self.request}).data
        equipment_images = models.CompanyServiceEquipmentImages.objects.bulk_create(
            [(models.CompanyServiceEquipmentImages(equipment=equipment, image=img)) for img in images])
        data["images"] = serializers.CompanyServiceEquipmentImagesSerializer(instance=equipment_images, many=True).data
        return Response(data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(company=user)
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}


class CompanyRatingViewSet(mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           GenericViewSet):
    serializer_class = serializers.CompanyRatingSerializer
    queryset = models.Rating.objects.all()
    permission_classes = [permissions.CompanyPermission]

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        company = self.request.user
        queryset = queryset.filter(company=company)
        return queryset


class CompanyContactsView(ListAPIView):
    queryset = models.CompanyContacts.objects.all()
    serializer_class = serializers.CompanyContactsSerializer
    permission_classes = [permissions.CompanyPermission]

    def get(self, request, **kwargs):
        user = self.request.user
        data = self.serializer_class(instance=user.company_contacts).data
        return Response(data)

    def patch(self, request):
        company = get_object_or_404(models.CompanyContacts, company=self.request.user.id)
        phone_number = self.request.data.get("phone_number")
        facebook = self.request.data.get("facebook")
        instagram = self.request.data.get("instagram")
        twitter = self.request.data.get("twitter")
        telegram = self.request.data.get("telegram")
        skype = self.request.data.get("skype")
        if phone_number:
            company.phone_number = phone_number
        if facebook:
            company.facebook = facebook
        if instagram:
            company.instagram = instagram
        if twitter:
            company.twitter = twitter
        if telegram:
            company.telegram = telegram
        if skype:
            company.skype = skype
        company.save()
        data = self.serializer_class(instance=company).data
        return Response(data, status=status.HTTP_200_OK)

