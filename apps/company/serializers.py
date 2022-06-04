from rest_framework import serializers
from apps.company import models
from apps.account import models as account_model


class CompanyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_model.Location
        exclude = ("id", "user")

    def create(self, validated_data):
        user = self.context.get("user")
        location = self.Meta.model.objects.get_or_create(user=user)[0]
        location.address = validated_data.get("address")
        location.lon = validated_data.get("lon")
        location.lat = validated_data.get("lat")
        location.save()
        return location


class CompanyServiceEquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyServiceEquipments
        exclude = ('id', 'company')


class CompanyServiceEquipmentImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyServiceEquipmentImages
        fields = ('id', 'image')


class CompanyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        exclude = ('appraiser',)

    def create(self, validated_data):
        appraiser = self.context['request'].user
        company = validated_data.get("company")
        try:
            rating = self.Meta.model.objects.get_or_create(appraiser=appraiser, **validated_data)[0]
            return rating
        except:
            raise serializers.ValidationError({'coach': "You should choose company for rating"})


class CompanyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyContacts
        exclude = ('id', 'company')
