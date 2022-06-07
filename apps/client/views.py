from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q

from apps.client import serializers
from apps.client import models
from apps.account import models as account_models
from apps.client import permissions
from apps.client import filter_params
from haversine import haversine


class CompanyViewForClient(mixins.ListModelMixin, GenericViewSet):
    queryset = account_models.CustomUser.objects.filter(user_type=account_models.CustomUser.COMPANY)
    serializer_class = serializers.CompanySerializerForClient
    permission_classes = [permissions.ClientPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryparams = self.request.query_params
        lon = float(queryparams.get('lon')) if queryparams.get('lon') else None
        lat = float(queryparams.get('lat')) if queryparams.get('lat') else None
        distance = float(queryparams.get('distance')) if queryparams.get('distance') else None
        near_dist_dict = {}
        null_dist_dict = {}
        print(distance)
        for i in queryset:
            try:
                dist = haversine((lat, lon), (i.user_location.lat, i.user_location.lon))
                if distance:
                    if dist < distance and dist is not None:
                        near_dist_dict[i] = dist
            except:
                if distance:
                    pass
                else:
                    null_dist_dict[i] = 0.0
        sort_data = sorted(near_dist_dict.items(), key=lambda x: x[1])
        sort_data += null_dist_dict.items()
        sorted_objects = [i[0] for i in sort_data]

        return sorted_objects

    @swagger_auto_schema(manual_parameters=filter_params.creators_filter_params())
    def list(self, request, *args, **kwargs):
        return super(CompanyViewForClient, self).list(kwargs)

    def get_serializer_context(self):
        queryparams = self.request.query_params
        lon = queryparams.get('lon')
        lat = queryparams.get('lat')
        return {
            "request": self.request,
            "lon": lon,
            "lat": lat
        }


class CompanyDetailForClientView(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = account_models.CustomUser.objects.filter(user_type=account_models.CustomUser.COMPANY)
    serializer_class = serializers.CompanyDetailForClientSerializer
    permission_classes = [permissions.ClientPermission]

    def get_serializer_context(self):
        return {"request": self.request}


class CompanySearchView(mixins.ListModelMixin, GenericViewSet):
    queryset = account_models.CustomUser.objects.filter(user_type=account_models.CustomUser.COMPANY)
    serializer_class = serializers.CompanySearchSerializer
    permission_classes = [permissions.ClientPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get("query")
        if query:
            queryset =queryset.filter(Q(first_name__icontains=query) |
                                      Q(last_name__icontains=query) |
                                      Q(username__icontains=query))
        queryset = queryset.order_by("?")
        return queryset

    @swagger_auto_schema(manual_parameters=filter_params.get_query())
    def list(self, request, *args, **kwargs):
        return super(CompanySearchView, self).list(kwargs)


class SavedCompanyViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    serializer_class = serializers.SavedCompanySerializer
    queryset = models.SavedCompany.objects.all()
    permission_classes = [permissions.ClientPermission]

    def create(self, request, *args, **kwargs):
        client = self.request.user
        company = self.request.data.get("company")
        is_company = get_object_or_404(account_models.CustomUser, id=company)
        if is_company and is_company.user_type == 'company':
            try:
                models.SavedCompany.objects.get(client=client, company_id=company).delete()
                return Response({"saved": False})
            except:
                models.SavedCompany.objects.create(client=client, company_id=company)
                return Response({"saved": True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You can save only company role"})


class SavedCompanyListView(mixins.ListModelMixin, GenericViewSet):
    queryset = models.SavedCompany.objects.all()
    serializer_class = serializers.SavedCompanySerializer
    permission_classes = [permissions.ClientPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(client=user)
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}
