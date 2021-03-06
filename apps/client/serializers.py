from rest_framework import serializers
from apps.account import models as account_model
from apps.client import models, modules
from apps.account import serializers as account_serializers
from haversine import haversine


class CompanySerializerForClient(serializers.ModelSerializer):
    class Meta:
        model = account_model.CustomUser
        fields = ('id', 'username', 'image', 'hourly_cost')

    def to_representation(self, instance):
        data = super(CompanySerializerForClient, self).to_representation(instance)
        stars = int(sum(instance.company_rating.filter(star__in=[1, 2, 3, 4, 5]).values_list('star', flat=True)))
        number_of_stars = instance.company_rating.filter(star__in=[1, 2, 3, 4, 5]).values_list('star',
                                                                                               flat=True).count()
        user = self.context.get("request").user
        user_lon = float(self.context.get("lon")) if self.context.get('lon') else None
        user_lat = float(self.context.get('lat')) if self.context.get('lat') else None
        data['star'] = 0
        try:
            rating = modules.calculate_star(stars/number_of_stars)
        except:
            rating = 0
        if stars > 0 and number_of_stars > 0:
            data['star'] = modules.calculate_star(a=stars, b=number_of_stars)

        try:
            data['location'] = account_serializers.UserLocationSerializer(instance=instance.user_location).data
        except:
            data['location'] = None
        try:
            data["distance"] = haversine((user_lat, user_lon),
                                         (instance.user_location.lat, instance.user_location.lon))
        except:
            data["distance"] = None
        return data


class CompanyDetailForClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_model.CustomUser
        fields = ("id", "username", "first_name", "last_name", "image", "hourly_cost", )

    def to_representation(self, instance):
        data = super(CompanyDetailForClientSerializer, self).to_representation(instance)
        stars = int(sum(instance.company_rating.filter(star__in=[1, 2, 3, 4, 5]).values_list('star', flat=True)))
        number_of_stars = instance.company_rating.filter(star__in=[1, 2, 3, 4, 5]).values_list('star',
                                                                                               flat=True).count()
        user = self.context.get("request").user

class CompanySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_model.CustomUser
        fields = ('id', 'first_name', 'last_name', 'image')

    def to_representation(self, instance):
        data = super(CompanySearchSerializer, self).to_representation(instance)
        stars = int(sum(instance.company_rating.filter(star__in=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
                        .values_list('star', flat=True)))
        num = instance.company_rating.filter(star__in=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]).\
            values_list("star", flat=True).count()
        data["location"] = None
        try:
            data["location"] = instance.user_location.address
        except:
            pass
        if stars and num:
            data["star"] = modules.calculate_star(stars,num)
        else:
            data["star"] = 0
        return data


class SavedCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SavedCompany
        exclude = ("client",)

    def to_representation(self, instance):
        data = super(SavedCompanySerializer, self).to_representation(instance)
        company = account_model.CustomUser.objects.get(id=instance.company.id)
        data['company'] = CompanySerializerForClient(instance=company,
                                                     context={"request": self.context["request"]}).data
        return data

